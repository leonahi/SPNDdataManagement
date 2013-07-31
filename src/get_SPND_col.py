import sqlite3 as lite


def get_columnNames(databaseName):
  con = lite.connect(databaseName)
  con.row_factory = lite.Row
  
  with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM sensor")
    row = cur.fetchone()    
    columnNames = row.keys()[3:]
    return tuple(columnNames)
    
def get_data(databaseName, sensorName):
  con = lite.connect(databaseName)
  
  columnNames = get_columnNames(databaseName)
  if sensorName in columnNames:
    with con:
      cur = con.cursor()
      cur.execute("SELECT {} FROM sensor".format(sensorName))    
      col = cur.fetchall()
      return col
  else:
    print("Error: Sensor name is not a valid sensor name")
    return None
  