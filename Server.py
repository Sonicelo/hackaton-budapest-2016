from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep, listdir
import os, random, itertools, urllib, pylsl
from mimetypes import MimeTypes
import urllib

# Web server configuration
PORT_NUMBER = 8080

info = pylsl.StreamInfo('MyMarkerStream', 'Markers', 1, 0, 'string', 'myuidw43536')

mime = MimeTypes()
outlet = pylsl.StreamOutlet(info)

all_pics = list()
list_samples = list()
list_data = list()
list_chain = list()

# This class will handles any incoming request from
# the browser

cur_index = 0
cur_time = 0

def gen_data():
    random.seed(123)
    global list_data, all_pics, list_samples, list_chain
    all_pics = list()
    list_samples = list()
    list_data = list()

    list_data = random.sample(next(os.walk('./www-data/images'))[1], 5)

    for a in list_data:
        temp = list()
        for b in listdir("./www-data/images/" + a):
            temp += random.sample([""+a+"/"+b+"/"+x for x in listdir("./www-data/images/" + a + "/" + b)], 6)
        list_samples.append(temp)
        for ah in list_samples:
            for bh in ah:
                if bh not in all_pics:
                    all_pics.append(bh)

    list_chain = list(itertools.chain.from_iterable(list_samples))

class myHandler(BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):
        global cur_time, cur_index, list_chain
        if self.path == "/":
            self.path = "/index.html"
        self.path = urllib.unquote(self.path).decode('utf8')

        try:
            mimeType = "application/json" # Default MIME type
            data = None

            if "data.json" in self.path:
                # Send next file (or done)
                if cur_time == 0:
                    outlet.push_sample(["start"])
                cur_time += 1
                cur_index = cur_time/20

                resp_type = "image"
                if cur_index == len(list_chain)-1:
                    cur_index = 0
                    cur_time = 0
                    gen_data()
                    outlet.push_sample(["done"])
                    resp_type = "done"

                data = '{"' + resp_type + '": "' + list_chain[cur_index] + '"}'

            elif "reset.json" in self.path:
                # Reset acquisition
                outlet.push_sample(["done"])
                gen_data()
                cur_index = 0
                cur_time = 0

            elif "all_images" in self.path:
                # TODO implement
                pass

            elif "markpoint" in self.path:
                # Send markpoint
                outlet.push_sample([list_chain[cur_index]])

            else:
                # Find out file MIME type
                mimeType = mime.guess_type(urllib.pathname2url(self.path))
                f = open(curdir + sep + 'www-data' + self.path)
                data = f.read()
                f.close()

            # Send response
            self.send_response(200)
            self.send_header("Content-type", mimeType)
            self.end_headers()

            # Along with data if applicable
            if data:
                self.wfile.write(data)

        except IOError, e:
            # Show muh errorz
            print e
            self.send_error(404, 'File Not Found: %s' % self.path)


try:
    # Create a web server and define the handler to manage the
    # incoming request

    gen_data()
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ', PORT_NUMBER

    # Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
