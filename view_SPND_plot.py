import matplotlib.pyplot as plt
from numpy import *
import os
import sys

dir_scr = os.path.join(os.getcwd(), "scr")
sys.path.insert(0, dir_scr)

from get_SPND_col import get_data  
  
def plot(databaseName, sensorName):
  data = get_data(databaseName, sensorName)
  data = array(data)
  plt.plot(data)
  plt.ylabel('Flux')
  plt.xlabel('Time in min')
  plt.show()