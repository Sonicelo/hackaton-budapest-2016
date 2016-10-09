from pylsl import StreamInlet, resolve_stream
import sys
import time
from threading import Thread

allData = list()
allMarkers = list()
go1 = True

def myData():
    global allData, go1
    streams1 = resolve_stream('name', 'filteredStream')
    inlet1 = StreamInlet(streams1[0])
    while go1:
        sample, timestamp = inlet1.pull_sample()
        print ",".join([str(a) for a in sample])+","+str(timestamp)

def myMarkers():
    global allMarkers
    streams2 = resolve_stream('name', 'FilteredStream-markers')
    inlet2 = StreamInlet(streams2[0])
    while len(allMarkers) < 45:
        sample, timestamp = inlet2.pull_sample()
        go1= False
        print "got %s at time %s" % (sample[0], timestamp)



t1 = Thread(target=myMarkers)
t1.start()

t2 = Thread(target=myData)
t2.start()
