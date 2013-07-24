# Main file that creates and joins database file(*.db) from SPND sensor data file(*.txt)

import argparse
import os
import sys
from create_database import read_SPND
from join_database import join_database
from name_creator import create_database_name, join_database_name
from view_SPND_plot import plot 


parser = argparse.ArgumentParser(description='Create two database and joining then together \
                                              or join two already created databse')
group = parser.add_mutually_exclusive_group()
#parser.add_argument("filename_1", help='Input file name-1 related to sensor data')
#parser.add_argument("filename_2", help='Input file name-2 related to sensor data')

group.add_argument("--createjoin", help='Create two database and join them together \
                   - For this input two sensor data file', nargs=2)

group.add_argument("--join", help='Join two already created database \
                   - For this input two database file', nargs=2)

group.add_argument("--plot", help="Generate single SPND sensor plot - \
                   For this input database file and the name of the sensor eg. --plot \
                   databaseFileName SPND29", nargs=2)

args = parser.parse_args()

if args.createjoin:
  print("Reading files {}, {}............".format(args.createjoin[0], args.createjoin[1]))
  print("Creating Database - 1.............")
  databaseName1 = create_database_name(args.createjoin[0])
  read_SPND(args.createjoin[0], databaseName1, "sensor")

  print("Creating Database - 2.............")
  databaseName2 = create_database_name(args.filename_2)
  read_SPND(args.createjoin[1], databaseName2, "sensor")

  databaseName3 = join_database_name(databaseName1, databaseName2)
  print("Joining Database - 1 and Database -2..............")
  join_database(databaseName1, databaseName2, databaseName3)
  print("Creating & Joining Database: Completed..........")

elif args.join:
  print("Reading files {}, {}............".format(args.join[0], args.join[1]))
  databaseName1 = create_database_name(args.join[0])
  databaseName2 = create_database_name(args.join[1])
  databaseName3 = join_database_name(databaseName1, databaseName2)  

  print("Joining Database - 1 and Database -2..............")
  join_database(args.join[0], args.join[1], databaseName3)
  print("Joining Database: Completed..........")
  
elif args.plot:
  print("Generating {} Plot.........".format(args.plot[1]))
  plot(args.plot[0], args.plot[1])
  print("Done..")