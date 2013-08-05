import sqlite3 as lite
import sys

def join_database(database1Name, database2Name, database3Name):
  ''' Join two database 'database1Name' and 'database2Name' which are created using create_database(), into database 'database3Name' '''
  
  con1 = lite.connect(database1Name)           # Connect to Database1
  con2 = lite.connect(database2Name)           # Connect to Database2
  con3 = lite.connect(database3Name)           # Connect to Database3

  con1.row_factory = lite.Row                  # For reading column names from Database1
  con2.row_factory = lite.Row                  # For reading column names from Database2

  con1_new = lite.connect(database1Name)       # Create new connection with Database1 for reading data
  con2_new = lite.connect(database2Name)       # Create new connection with Database2 for reading data

  with con1, con2, con3, con1_new, con2_new:
    cur1 = con1.cursor()
    cur2 = con2.cursor()
    cur3 = con3.cursor()
  
    cur1_new = con1_new.cursor()
    cur2_new = con2_new.cursor()
  
    cur1.execute("SELECT * FROM sensor")
    cur2.execute("SELECT * FROM sensor")
  
    row_1 = cur1.fetchone()
    row_2 = cur2.fetchone()
  
    columnNames = row_1.keys()        # Read column names from Database1
    
    #print(row_2.keys())
    #print(row_1.keys())
    for item in row_2.keys():         # Append column names from Database1 with Database2, removing the duplicate column names
      if item not in row_1.keys():
        columnNames.append(item)
  
    cur3.execute("CREATE TABLE IF NOT EXISTS sensor(Id INTEGER PRIMARY KEY, Date TEXT(10), Time TEXT(8))")
    
    #print(columnNames[3:])
    for col in columnNames[3:]:      # Create SPND columns (SPND29, SPND30.....). Exclude Id, Date and Time
      cur3.execute("ALTER TABLE sensor ADD {} DOUBLE".format(col))
  
    cur1_new.execute("SELECT * FROM sensor")
    cur2_new.execute("SELECT * FROM sensor")
  
    rows1 = cur1_new.fetchall()      # Read all rows from Database1 
    rows2 = cur2_new.fetchall()      # Read all rows from Database2
  
    rows1 = [r[1:] for r in rows1]   # Read Date, Time and all sensor data
    rows2 = [r[3:] for r in rows2]   # Read only sensor data
  
    rows = [r1 + r2 for r1, r2 in zip(rows1, rows2)]   # Combine each rows in Database1 and Database2 element wise
  
    ques = []                        # Use by sqlite for inserting into table
    
    ques = ["?"]*len(columnNames[1:])
    ques = ",".join(ques)
    
    columnNames = ",".join(columnNames[1:])
      
    #print(ques)
    #print(columnNames)
    #print(rows[0])
    #print(len(rows))
    for item in rows:                # Insert combined data into new Database3
      cur3.execute("INSERT INTO sensor({0}) VALUES ({1})".format(columnNames, ques), item)
      
if __name__ == '__main__':
  pass
  #join_database("SPND_Database/10F29-130.db", "SPND_Database/10SPND1-42.db", "F29-130_SPND1-42.db")