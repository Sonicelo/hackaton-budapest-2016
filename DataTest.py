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
        allData.append([str(a) for a in sample]+[timestamp])


def myMarkers():
    global allMarkers
    streams2 = resolve_stream('name', 'FilteredStream-markers')
    inlet2 = StreamInlet(streams2[0])
    while len(allMarkers) < 40:
        sample, timestamp = inlet2.pull_sample()
        go1 = False
        allMarkers.append([sample[0], timestamp])

def touch(fname, times=None):
    fhandle = open(fname, 'a')
    try:
        os.utime(fname, times)
    finally:
        fhandle.close()


def between(l1, low, high):
    l2 = []
    for i in l1:
        if low <= i[-1] <= high:
            l2.append(i)
    return l2

t1 = Thread(target=myMarkers)
t1.start()

t2 = Thread(target=myData)
t2.start()

while len(allMarkers) < 40:
    time.sleep(1)


for index in range(1, len(allMarkers)-2, 1):
    marker = allMarkers[index-1][0]
    pos1 = allMarkers[index-1][1]
    pos2 = allMarkers[index][1]

    data = between(allData, pos1, pos2)
    for d in data:
        touch(str("samples/"+marker.replace("/", "_").replace(" ", "_")+"sample.txt"))
        with open(str("samples/"+marker.replace("/", "_").replace(" ", "_")+"sample.txt"), "a+") as f:
            f.write(",".join([str(a) for a in d])+"\n")


print "done"