# Main file that creates and joins database file(*.db) from SPND sensor data file(*.txt)


import argparse
import os
from create_database import read_SPND
from join_database import join_database
from name_creator import create_database_name, join_database_name


parser = argparse.ArgumentParser(description='Create two database and joining then together \
                                              or join two already created databse')
group = parser.add_mutually_exclusive_group()
parser.add_argument("filename_1", help='Input file name-1 related to sensor data')
parser.add_argument("filename_2", help='Input file name-2 related to sensor data')

group.add_argument("--createjoin", help='Create two database and join them together \
                   - For this input two sensor data file', action='store_true')

group.add_argument("--join", help='join two already created database \
                   - For this input two database file', action='store_true')

group.add_argument("--create", help="create database - For this input single sensor data file", action='store_true')

args = parser.parse_args()
print("Reading files {}, {}............".format(args.filename_1, args.filename_2))

if args.createjoin:
  print("Creating Database - 1.............")
  databaseName1 = create_database_name(args.filename_1)
  print(args.filename_1)
  read_SPND(args.filename_1, databaseName1, "sensor")

  print("Creating Database - 2.............")
  databaseName2 = create_database_name(args.filename_2)
  read_SPND(args.filename_2, databaseName2, "sensor")

  databaseName3 = join_database_name(databaseName1, databaseName2)
  print("Joining Database - 1 and Database -2..............")
  join_database(databaseName1, databaseName2, databaseName3)
  print("Creating & Joining Database: Completed..........")

elif args.join:
  databaseName1 = create_database_name(args.filename_1)
  databaseName2 = create_database_name(args.filename_2)
  databaseName3 = join_database_name(databaseName1, databaseName2)  

  print("Joining Database - 1 and Database -2..............")
  join_database(args.filename_1, args.filename_2, databaseName3)
  print("Joining Database: Completed..........")
