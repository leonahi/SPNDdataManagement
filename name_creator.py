import os

def create_database_name(filename):
  ''' Creates database name from input sensor data file'''   
                                                                 # filename = /path/to/file/10 SPND1-7.ext (Note. This eg filename contains cobalt data)
  directory, filename = os.path.split(filename)                  # directory = /path/to/file/    filename = 10 SPND1-7.ext
  databaseName = os.path.splitext(filename)                      # databaseName[0] = 10 SPND1-7, databaseName[1] = .ext
  databaseName = "".join(databaseName[0].split())                # databaseName = ['10', 'SPND1-7']
  databaseName = os.path.join(directory,databaseName) + ".db"    # databaseName = /path/to/file/10SPND1-7.db
  return databaseName

def join_database_name(dbfilename1, dbfilename2):
  ''' Creates database name by joining two database name'''
  directory1, dbfilename1 = os.path.split(dbfilename1)
  directory2, dbfilename2 = os.path.split(dbfilename2)
  databaseName3 = (os.path.splitext(dbfilename1))[0] + (os.path.splitext(dbfilename2))[0]  # eg. 10F29-3510F36-42 = 10F29-35 + 10F36-42
  databaseName3 = databaseName3.split("-")                                                     # eg. [10F29, 3510F36, 42] = split(10F29-3510F36-42)
  if len(databaseName3) == 2:
    databaseName3 = os.path.join(directory1,databaseName3[0]) + "-" + "106" + ".db"
  else:
    databaseName3 = os.path.join(directory1,databaseName3[0]) + "-" + databaseName3[2] + ".db"     # eg. 10F29-42.db = 10F29 + '-' + 42 + '.db'
  return databaseName3
