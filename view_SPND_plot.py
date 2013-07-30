import matplotlib.pyplot as plt
import numpy
import os
import sys

dir_scr = os.path.join(os.getcwd(), "scr")
sys.path.insert(0, dir_scr)

from get_SPND_col import get_data  
  
def plot(databaseName, sensorName):
  data = get_data(databaseName, sensorName)
  data = numpy.array(data).astype(float)
  
  if sensorName[0] == 'V':
    data = (numpy.divide(data,numpy.max(numpy.abs(data))))*100
  
  plt.title("{} data".format(sensorName))
  plt.plot(data)
  plt.axis([0,16000,0,100])
  plt.ylabel('Flux')
  plt.xlabel('Time in min')
  plt.show()