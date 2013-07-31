import sys, os

def initialize():
  dir_cwd = os.getcwd()                               # Add current working directory into python search path
  sys.path.insert(0, dir_cwd)

  dir_src = os.path.join(os.getcwd(), "src")          # Add src directory into python search path
  sys.path.insert(0, dir_src)


