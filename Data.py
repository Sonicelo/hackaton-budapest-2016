import pandas
import os
import numpy

for a in os.listdir("samples/"):
    data_df = pandas.read_csv("samples/"+a)[:1]
    numpyMatrix = data_df.as_matrix()
    for a in numpyMatrix:
        print [a*b for a, b in zip(a, numpy.hamming(len(a)))]
