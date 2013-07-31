import cProfile
import pstats
import sys, os

sys.path.insert(0, "/home/nahit/BARC_PROJECT/double-dragon/")
from read_database import read_database

cProfile.run("read_database('SPND_Database/Vanadium/10F29-130.db')")
#cProfile.run("read_database('SPND_Database/Vanadium/10F29-130.db')", "profilingData_read_database.tmp")
#stat = pstats.Stats("profilingData_read_database.tmp")
#stat.print_stats()