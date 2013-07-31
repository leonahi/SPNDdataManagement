# Main file that creates and joins database file(*.db) from SPND sensor data file(*.txt)

import argparse
import os
import sys
import subprocess

from init_dd import initialize

from create_database import read_SPND_V, read_SPND_Co
from append_database import append_database
from join_database import join_database
from name_creator import create_database_name, join_database_name
from view_SPND_plot import plot 

#initialize()

parser = argparse.ArgumentParser(description='Create two database and joining then together \
                                              or join two already created databse')

group1 = parser.add_mutually_exclusive_group(required=True)
group1.add_argument("--append", help="Append new data from another database", nargs=2)
group1.add_argument("--createjoin", help='Create two database and join them together \
                   - For this input two sensor data file', nargs=2)
                   
group1.add_argument("--join", help='Join two already created database \
                   - For this input two database file', nargs=2)
                   
group1.add_argument("--plot", help="Generate single SPND sensor plot - \
                   For this input database file and the name of the sensor eg. --plot \
                   databaseFileName SPND29", nargs=2)

group2 = parser.add_mutually_exclusive_group()
group2.add_argument("-v", "--vanadium", help="If input sensor data file is of Vanadium", action='store_true')
group2.add_argument("-c", "--cobalt", help="If input sensor data file is of Cobalt", action='store_true')
                   
                   
args = parser.parse_args()

if args.createjoin and args.vanadium:
  print("Reading files {}, {}............".format(args.createjoin[0], args.createjoin[1]))
  print("Creating Database - 1.............")
  databaseName1 = create_database_name(args.createjoin[0])
  read_SPND_V(args.createjoin[0], databaseName1, "sensor")

  print("Creating Database - 2.............")
  databaseName2 = create_database_name(args.createjoin[1])
  read_SPND_V(args.createjoin[1], databaseName2, "sensor")

  databaseName3 = join_database_name(databaseName1, databaseName2)
  print("Joining Database - 1 and Database -2..............")
  join_database(databaseName1, databaseName2, databaseName3)
  print("Creating & Joining Database: Completed")

elif args.createjoin and args.cobalt:
  print("Reading files {}, {}............".format(args.createjoin[0], args.createjoin[1]))
  print("Creating Database - 1.............")
  databaseName1 = create_database_name(args.createjoin[0])
  read_SPND_Co(args.createjoin[0], databaseName1, "sensor")

  print("Creating Database - 2.............")
  databaseName2 = create_database_name(args.createjoin[1])
  read_SPND_Co(args.createjoin[1], databaseName2, "sensor")

  databaseName3 = join_database_name(databaseName1, databaseName2)
  print("Joining Database - 1 and Database -2..............")
  join_database(databaseName1, databaseName2, databaseName3)
  print("Creating & Joining Database: Completed")

elif args.join:
  print("Reading files {}, {}............".format(args.join[0], args.join[1]))
  databaseName1 = create_database_name(args.join[0])
  databaseName2 = create_database_name(args.join[1])
  databaseName3 = join_database_name(databaseName1, databaseName2)  

  print("Joining Database - 1 and Database -2..............")
  join_database(args.join[0], args.join[1], databaseName3)
  print("Joining Database: Completed..........")
  
elif args.append:
  print("Inserting new data into database {}".format(args.append[0]))
  append_database(args.append[0], args.append[1])
  print("Done..")
  
elif args.plot:
  print("Generating {} Plot.........".format(args.plot[1]))
  plot(args.plot[0], args.plot[1])
  print("Done..")
  
else:
  print("Pass --help option for more information")