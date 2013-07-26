import sqlite3 as lite
import sys
import re

''' Contains two funtion read_SPND_V and read_SPND_Co'''


#------------------------------------------------read_SPND_V--------------------------------------------------

def read_SPND_V(fileName, databaseName, tableName):
  fd = open(fileName, encoding='utf-8', mode='r')
  
  con = lite.connect(databaseName)
  con.row_factory = lite.Row 
  
  with con, fd:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS {0}(Id INTEGER PRIMARY KEY, Date TEXT(10), Time TEXT(8))".format(tableName)) # Create Columns Id, Date and Time

    ''' Creating one column per SPND '''
    lineNumber = 0
    sensorList = []
    sensorNumber = 0
    for line in fd:
      if lineNumber < 10:
        lst = line.split()
        if len(lst) != 8:
          lineNumber += 1
          continue
        sensorNumber = lst[5]
        cur.execute("ALTER TABLE {0} ADD V{1} DOUBLE".format(tableName, sensorNumber))
        sensorList.append("V{}".format(sensorNumber))
      else:
        break
      lineNumber += 1
    
    numSensor  = len(sensorList)               # Number of sensor in single file
    sensorList = ",".join(sensorList)          # Contains names of the sensor eg-SPND29, SPND30....etc
    ques = ["?"]*numSensor                     # Used in Sql query
    ques = ",".join(ques)                      # used in sql query
    #print(sensorList)
    #print(numSensor)
    fd.seek(0)
    
    
    ''' Inserting data into columns '''
    pattern = "BAD|NORPLY"                   # Pattern to detect any occurrence of BAD, NORPLY
    lineNumber = 0
    for line in fd:      
      if lineNumber >= 12:
        lst = line.split()
        date_time = lst[0].split('-')
        date_time = tuple(date_time)
        lst = [re.sub(r'\b{0}\b'.format(pattern), '-1', item) for item in lst[1:]]        # replace any occurrence of BAD, NORPLY with -1
        if int(sensorNumber) > 106:
          sensorData = tuple(lst)
        else:
          sensorData = tuple(lst[1:])  
        data = date_time + sensorData
        cur.execute("INSERT INTO {0} (Date, Time, {1}) VALUES (?, ?, {2})".format(tableName, sensorList, ques), data)	  
      lineNumber = lineNumber + 1  
    
    
    con.commit()
    
if __name__ == '__main__':
  pass
  #read_SPND("13 F78-84.txt", "13F78-84.db", "sensor")

  
#------------------------------------------------read_SPND_Co--------------------------------------------------  

def read_SPND_Co(fileName, databaseName, tableName):
  fd = open(fileName, encoding='utf-8', mode='r')
  
  con = lite.connect(databaseName)
  con.row_factory = lite.Row 
  
  with con, fd:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS {0}(Id INTEGER PRIMARY KEY, Date TEXT(10), Time TEXT(8))".format(tableName)) # Create Columns Id, Date and Time

    ''' Creating one column per SPND '''
    lineNumber = 0
    sensorList = []
    sensorNumber = 0
    for line in fd:
      if lineNumber < 10:
        lst = line.split()
        if len(lst) != 7:
          lineNumber += 1
          continue
        sensorNumber = lst[2]
        cur.execute("ALTER TABLE {0} ADD Co{1} DOUBLE".format(tableName, sensorNumber))
        sensorList.append("Co{}".format(sensorNumber))
      else:
        break
      lineNumber += 1
    
    numSensor  = len(sensorList)               # Number of sensor in single file
    sensorList = ",".join(sensorList)          # Contains names of the sensor eg-SPND29, SPND30....etc
    ques = ["?"]*numSensor                     # Used in Sql query
    ques = ",".join(ques)                      # used in sql query
    #print(sensorList)
    #print(numSensor)
    fd.seek(0)
    
    
    ''' Inserting data into columns '''
    pattern = "BAD|NORPLY"                   # Pattern to detect any occurrence of BAD, NORPLY
    lineNumber = 0
    for line in fd:      
      if lineNumber >= 12:
        lst = line.split()
        date_time = lst[0].split('-')
        date_time = tuple(date_time)
        lst = [re.sub(r'\b{0}\b'.format(pattern), '-1', item) for item in lst[1:]]        # replace any occurrence of BAD, NORPLY with -1
        if int(sensorNumber) > 106:
          sensorData = tuple(lst)
        else:
          sensorData = tuple(lst[1:])  
        data = date_time + sensorData
        cur.execute("INSERT INTO {0} (Date, Time, {1}) VALUES (?, ?, {2})".format(tableName, sensorList, ques), data)	  
      lineNumber = lineNumber + 1  
    
    
    con.commit()
    
if __name__ == '__main__':
  pass
  read_SPND_V("10 F123-130.txt", "10F123-130.db", "sensor")  
  
  
  