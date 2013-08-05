import sqlite3 as lite

def append_database(databaseName1, databaseName2, sensorType=None):
  
  con1 = lite.connect(databaseName1)
  con2 = lite.connect(databaseName2)
  
  with con2:
    con2.row_factory = lite.Row
    cur2 = con2.cursor()
    cur2.execute("SELECT * FROM sensor")
  
    columnNames = cur2.fetchone().keys()
  
  
  numOfColumns = len(columnNames)-1       # Exclude Id 
  ques = ['?']*numOfColumns
  ques = ",".join(ques)
  columnNames = ",".join(columnNames[1:])
  
  con2 = lite.connect(databaseName2)
  
  with con1, con2:    
    cur1 = con1.cursor()
    cur2 = con2.cursor()
    
    cur2.execute("SELECT * FROM sensor")
    
    data = cur2.fetchall()
    for row in data:
      cur1.execute("INSERT INTO sensor ({0}) VALUES ({1})".format(columnNames,ques), row[1:])
      
      
if __name__ == "__main__":
  pass
  #append_database("10F29-130.db", "11F29-130.db")