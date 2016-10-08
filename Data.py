#! /usr/bin/env python



import time
import json
try:
    from urllib.parse import urlparse  # Python 3
except ImportError:
    from urlparse import urlparse  # Python 2


import requests
import paho.mqtt.client as mqtt
import msgpack
import pylsl


api_url = 'https://api.neuroscale.io'


access_token = '<your-access-token>'

auth_header = {'Authorization': 'Bearer ' + access_token}

pipeline_name = 'Highpass'

instance_id = ''

input_stream = 'OutStream'


output_stream = 'ReceivedStream'

print("looking for the input stream '%s'..." % input_stream)
streams = pylsl.resolve_stream('name', input_stream)

inlet = pylsl.StreamInlet(streams[0])
info = inlet.info()
sampling_rate = info.nominal_srate()
modality = info.type()
desc = info.desc()
try:
    channel_labels = []
    ch = desc.child('channels').child('channel')
    while not ch.empty():
        channel_labels.append(ch.child_value('label') or '(no label)')
        ch = ch.next_sibling('channel')
    if len(set(channel_labels)) < len(channel_labels):
        raise RuntimeError("Channel labels are not unique!")
    if len(channel_labels) != info.channel_count():
        raise RuntimeError("Incorrect number of channel labels!")
except Exception as e:
    print("Error parsing channel labels: %s; falling back to defaults" % e)

    channel_labels = ['Ch' + str(k) for k in range(info.channel_count())]

outinfo = pylsl.StreamInfo(output_stream, 'EEG', len(channel_labels),
                           sampling_rate, 'float32', 'mystream-f8yuewfu')
outlet = pylsl.StreamOutlet(outinfo)


r = requests.get(api_url + '/v1/pipelines', headers=auth_header)
if r.status_code == 200:
    body = r.json()
    pipelines = body['data']

    for p in pipelines:
        if p['name'] == pipeline_name:
            pipeline_id = p['id']
            break
    else:
        print("ERROR: Could not find a pipeline named '%s'" % pipeline_name)
        exit(1)
else:
    print("ERROR: Could not query available pipelines (HTTP %s); check "
          "your API URL and credentials." % r.status_code)
    exit(1)

eeg_stream = {"name": "myeeg", "type": modality, "sampling_rate": sampling_rate,
              "channels": [{"label": c} for c in channel_labels]}

node_decl = {"name": "default", "streams": [eeg_stream]}

metadata = {"nodes": {"in": [node_decl], "out": [node_decl]}}

json_fallback = False

params = {"pipeline": pipeline_id, "metadata": metadata,
          "encoding": 'json' if json_fallback else 'msgpack'}

if not instance_id:
    r = requests.post(api_url + '/v1/instances', headers=auth_header, json=params)
else:
    r = requests.patch(api_url + '/v1/instances/' + instance_id,
                       headers={'Authorization': auth_header['Authorization'],
                                'Content-Type': 'application/json'},
                       data=json.dumps(params))
if r.status_code == 201 or r.status_code == 200:
    reader = read_endpoint = None

    body = r.json()
    instance_id = body['id']
    try:
        print('instance %s has been requested successfully' % instance_id)


        print('waiting for instance to come up...')
        last_state = ''
        while last_state != 'running':

            r = requests.get(api_url + '/v1/instances/' + instance_id,
                             headers=auth_header)
            state = r.json()["state"]
            if state != last_state:
                print(state + "...")
                last_state = state
            time.sleep(1)


        def get_endpoint(x, mode='read'):
            url = [e['url'] for e in x['endpoints']['data'] if e['mode'] == mode]
            return urlparse(url[0])
        read_endpoint = get_endpoint(body, mode='read')
        write_endpoint = get_endpoint(body, mode='write')

        def on_connect(client, userdata, flags, rc):
            print("%s connected with result code %s" % (userdata, rc))

            if userdata == 'reader':

                client.subscribe('/' + str(read_endpoint.path[1:]) + '/#')

        def on_message(client, userdata, msg):

            topic = msg.topic.split('/')[-1]
            if topic != 'default':
                print("received message on non-default topic (%s); ignoring."
                      % topic)

            payload = msg.payload
            data = json.loads(payload) if json_fallback else msgpack.loads(payload)

            streams = data[b'streams']
            if streams:
                print('received message on topic %s: ' % msg.topic)
            else:
                print('received empty message on topic %s: ' % msg.topic)
            for stream in streams:

                name = stream[b'name']

                samples = stream[b'samples']

                stamps = stream[b'timestamps']

                if name == b'myeeg':
                    outlet.push_chunk(samples)
                print('  stream %s: %i samples' %
                      (name, len(stamps)))

        def on_disconnect(client, userdata, *args):
            print("%s got disconnected." % userdata)
            if userdata == 'reader':
                reader.connect(read_endpoint.hostname, read_endpoint.port)
            else:
                writer.connect(write_endpoint.hostname, write_endpoint.port)

        def on_subscribe( client, userdata, mid, granted_qos ):
            print("%s subscribed at quos level %s" % (userdata, granted_qos))

        def on_publish( client, userdata, mid ):
            print("%s has published." % userdata)

        def on_unsubscribe(client, userdata, *args):
            print("%s got unsubscribed." % userdata)


        reader = mqtt.Client(userdata='reader')
        reader.on_connect = on_connect
        reader.on_subscribe = on_subscribe
        reader.on_message = on_message
        reader.on_disconnect = on_disconnect
        reader.on_unsubscribe = on_unsubscribe
        reader.connect(read_endpoint.hostname, read_endpoint.port)
        reader.loop_start()

        writer = mqtt.Client(userdata='writer')
        writer.on_connect = on_connect
        writer.on_publish = on_publish
        writer.on_disconnect = on_disconnect
        writer.on_unsubscribe = on_unsubscribe
        writer.connect(write_endpoint.hostname, write_endpoint.port)
        writer.loop_start()


        print('now sending data...')
        while True:

            samples, timestamps = inlet.pull_chunk()
            if timestamps:
                print("Got new chunk from LSL (len=%s)..." % len(timestamps))


                eeg_chunk = {'name': 'myeeg', 'samples': samples,
                             'timestamps': timestamps}

                msg = {'streams': [eeg_chunk]}

                if json_fallback:
                    msg = json.dumps(msg)
                else:
                    msg = bytearray(msgpack.dumps(msg))


                writer.publish('/' + str(write_endpoint.path[1:]), msg)


            time.sleep(0.1)

    except Exception as ex:
        print("ERROR: %s" % ex)
    finally:
        if reader:
            reader.unsubscribe('/' + str(read_endpoint.path[1:]) + '/#')
            time.sleep(0.5)

        kill = ''
        while kill not in ['y', 'n']:
            try:
                kill = raw_input('Kill the instance? (y/n):')  # Python 2.x
            except NameError:
                kill = input('Kill the instance? (y/n):')  # Python 3.x
        if kill == 'y':
            r = requests.delete(api_url + '/v1/instances/' + instance_id,
                                headers=auth_header)
            if r.status_code == 204:
                print('instance %s was deleted successfully' % instance_id)
            else:
                print('ERROR: instance %s was not deleted (HTTP %i)' %
                      (instance_id, r.status_code))
else:
print('ERROR: could not bring up instance (HTTP %i)' % r.status_code)