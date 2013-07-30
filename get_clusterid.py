import sqlite3 as lite
import Pycluster as cluster
import numpy

def get_clusterid(vanadium_dbName, Cobalt_dbName):
  ''' Given the database of sensor observation it calculates clusterid for each sensor'''
  con = lite.connect(vanadium_dbName)
  con.row_factory = lite.Row
  
  with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM sensor")    
    columnNames = cur.fetchone()
    columnNames = columnNames.keys()
    
  con = lite.connect(vanadium_dbName)
  with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM sensor")    
    rows = cur.fetchall()
    
  ROW = [row[3:] for row in rows]
  
  Data = numpy.matrix(ROW).astype(float)
  Data = numpy.transpose(Data)            
  
  numRows, numCols = Data.shape
  
  mask = numpy.ones((numRows, numCols)).astype(numpy.uint8)     
  counter = 0
  for i in range(numRows):
    for j in range(numCols):
      if Data[i,j] < 0:
        counter += 1                      # Counting the missing observation
        mask[i,j] = 0
  
  
  clusterid, error, nfound = cluster.kcluster(data=Data, nclusters=7, 
                                        mask=mask, weight=None,
                                        transpose=0, npass=1,
                                        method='a', dist='c', initialid=None)      
  
  
  '''Create clusterid to SPND dictonary'''
  clusterIdtoSPND = {}
  lst = []
  for cid in clusterid:
    clusterIdtoSPND[cid] = lst
  for cid, col in zip(clusterid, columnNames[3:]):
    clusterIdtoSPND[cid].append(col)  
  
  
  #print("Number of missing observation : {}".format(counter))
  #print("No. of rows : {}, No. of Cols : {}".format(numRows, numCols))
  #print()
  
if __name__ == "__main__":
  get_clusterid("SPND_Database/Vanadium/10F29-130.db", "SPND_Database/Cobalt/10SPND1-42.db" )