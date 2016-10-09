import pandas
import os
import scipy
import numpy
import matplotlib.pyplot as pyplot

pyplot.ion()
pyplot.show()


for a in os.listdir("samples/"):
    data_df = pandas.read_csv("samples/"+a)[1:]

    numpyMatrix = data_df.as_matrix()[900:]

    print numpyMatrix
    try:
        pyplot.plot(numpy.fft.fft(numpyMatrix[:, 1])[100:])
        pyplot.draw()
        pyplot.pause(1)
    except:
        print a