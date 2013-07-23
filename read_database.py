import sqlite3 as lite
from Pycluster import *
from numpy import *

def read_database(databaseName):
  ''' Read databaseName and return data array in the format as required by Pycluster module'''
  
  con = lite.connect(databaseName)
  con.row_factory = lite.Row
  
  con_new = lite.connect(databaseName)
  
  with con, con_new:
    cur = con.cursor()
    cur_new = con_new.cursor()
    
    cur.execute("SELECT * FROM sensor")
    
    columnNames = cur.fetchone()
    columnNames = columnNames.keys()
    
    cur_new.execute("SELECT * FROM sensor")
    rows = cur_new.fetchall()
    
    rows = [row[3:] for row in rows]
    
    Data = matrix(rows)
    
    rc = Data.shape
    mask = ones((rc[0], rc[1]))    
    mask = matrix(mask)
    
    for i in range(Data.shape[0]):
      for j in range(Data.shape[1]):
        if Data[i,j] < 0:
          #print(Data[i,j])
          mask[i,j] = 0

    #mask = mask.transpose()
    
    clusterid, error, nfound = kcluster(data=Data, nclusters=7, 
                                        mask=mask, weight=None,
                                        transpose=1, npass=50,
                                        method='a', dist='c', initialid=None)
                                        
    print(clusterid)
    print(nfound)
    print(error)
    
    SPNDtoClusterId = {col:cid for col, cid in zip(columnNames[3:], clusterid)}
    
    
    #SPNDtoClusterId = {print("{} : {}".format(col,cid)) for col, cid in zip(columnNames[3:], clusterid)}
    #print(clusterid.shape)    
    
    #print(zeros(9).reshape(3,3))
    
    #print(columnNames)
    #print(Data[0,0])
    #print(Data.shape)
    #print(mask)
    
if __name__ == '__main__':
  read_database("SPND_Database/10F29-130.db")