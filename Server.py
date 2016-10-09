from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import os, random, itertools, urllib, pylsl


PORT_NUMBER = 8080

info = pylsl.StreamInfo('MyMarkerStream', 'Markers', 1, 0, 'string', 'myuidw43536')


outlet = pylsl.StreamOutlet(info)

all_pics = list()
list_samples = list()
list_data = list()

list_chian = list()

# This class will handles any incoming request from
# the browser

cur_index = 0
cur_time = 0

def gen_data():
    random.seed(123)
    global list_data, all_pics, list_samples, list_chian
    all_pics = list()
    list_samples = list()
    list_data = list()

    list_data = random.sample(next(os.walk('./www-data/images'))[1], 5)

    for a in list_data:
        temp = list()
        for b in os.listdir("./www-data/images/" + a):
            temp += random.sample([""+a+"/"+b+"/"+x for x in os.listdir("./www-data/images/" + a + "/" + b)], 6)
        list_samples.append(temp)
        for ah in list_samples:
            for bh in ah:
                if bh not in all_pics:
                    all_pics.append(bh)

    list_chian = list(itertools.chain.from_iterable(list_samples))


class myHandler(BaseHTTPRequestHandler):
    # Handler for the GET requests
    def do_GET(self):
        global cur_time, cur_index, list_chian
        if self.path == "/":
            self.path = "/index.html"
        self.path = urllib.unquote(self.path).decode('utf8')

        try:
            # Check the file extension required and
            # set the right mime type

            sendReply = False
            if "data.json" in self.path:
                if cur_time == 0:
                    outlet.push_sample(["start"])
                cur_time += 1
                cur_index = cur_time/20

                if cur_index == len(list_chian)-1:
                    cur_index = 0
                    cur_time = 0
                    gen_data()
                    outlet.push_sample(["done"])
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write('{"done": "' + list_chian[cur_index] + '"}')
                else:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write('{"image": "' + list_chian[cur_index] + '"}')
                return
            elif "reset.json" in self.path:
                outlet.push_sample(["start"])
                gen_data()
                cur_index = 0
                cur_time = 0
            elif "markpoint" in self.path:
                outlet.push_sample(list_chian[cur_index])
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write("  ")


            else:
                if self.path.endswith(".html"):
                    mimetype = 'text/html'
                    sendReply = True
                if self.path.endswith(".jpg"):
                    mimetype = 'image/jpg'
                    sendReply = True
                if self.path.endswith(".jpeg"):
                    mimetype = 'image/jpeg'
                    sendReply = True
                if self.path.endswith(".gif"):
                    mimetype = 'image/gif'
                    sendReply = True
                if self.path.endswith(".png"):
                    mimetype = 'image/png'
                    sendReply = True
                if self.path.endswith(".js"):
                    mimetype = 'application/javascript'
                    sendReply = True
                if self.path.endswith(".css"):
                    mimetype = 'text/css'
                    sendReply = True
                if self.path.endswith(".json"):
                    mimetype = 'application/json'
                    sendReply = True

                if sendReply == True:
                    # Open the static file requested and send it

                    f = open(curdir + sep + 'www-data' + self.path)
                    self.send_response(200)
                    self.send_header('Content-type', mimetype)
                    self.end_headers()
                    self.wfile.write(f.read())
                    f.close()
                return


        except IOError, e:
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