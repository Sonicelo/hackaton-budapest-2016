from pylsl import StreamInlet, resolve_stream
import sys
import time
import os
import urllib
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
        allData.append([",".join([str(a) for a in sample])+","+str(timestamp)])


def myMarkers():
    global allMarkers
    streams2 = resolve_stream('name', 'FilteredStream-markers')
    inlet2 = StreamInlet(streams2[0])
    while len(allMarkers) < 40:
        sample, timestamp = inlet2.pull_sample()
        go1 = False
        allMarkers.append(sample[0])

def touch(fname, times=None):
    fhandle = open(fname, 'a')
    try:
        os.utime(fname, times)
    finally:
        fhandle.close()


t1 = Thread(target=myMarkers)
t1.start()

t2 = Thread(target=myData)
t2.start()

while len(allMarkers) < 40:
    time.sleep(1)

for marker in allMarkers:
    touch(str("samples/"+marker.replace("/", "_").replace(" ", "_")+"sample.txt")[50:])
    with open(str("samples/"+marker.replace("/", "_").replace(" ", "_")+"sample.txt")[50:], "w+") as f:
        for line in allData[allMarkers.index(marker)]:
            f.write(line+"\n")


print "done"