from tkinter import *
from tkinter.filedialog import *
import tkinter.ttk as ttk
import Pmw
import os
import sys
import subprocess
from name_creator import create_database_name, join_database_name

dir_src = os.path.join(os.getcwd(), "src")
sys.path.insert(0, dir_src)

from get_SPND_col import get_columnNames, get_data


class GUI():
  
  file_opt = {}
  file_opt_DB = {}
  opt = []
  row_counter = 0
  filename1 = ""
  filename2 = ""
  sensorNames = ()
  
  def __init__(self, parent):
    self.master = parent
    self.master.title("Double-Dragon")
    
    self.file_opt['defaultextension'] = '.txt'
    self.file_opt['filetypes'] = [('text files', '.txt'), ('db files', '.db')]
    self.file_opt['parent'] = self.master
    self.file_opt['title'] = 'Open file'
   
    self.file_opt_DB['defaultextension'] = '.db'
    self.file_opt_DB['filetypes'] = [('db files', '.db')]
    self.file_opt_DB['parent'] = self.master
    self.file_opt['title'] = 'Open file'
    
    self.menubar = Menu(parent)
    parent.config(menu=self.menubar)
    
    self.fileMenu = Menu(self.menubar)
    self.menubar.add_cascade(label='File', menu=self.fileMenu)
    
    self.fileMenu.add_command(label='Quit', command=self.master.quit)
    
    
    self.createButton(parent=parent, label="Open File 1 :", command=self.openfile1,  col=0, row=0, padx=10, pady=10)
    self.createButton(parent=parent, label="Open File 2 :", command=self.openfile2,  col=0, row=1, padx=10, pady=10)
    
    self.label_str1 = StringVar()
    self.label_str1.set("filename 1.db/txt")
    
    self.label_str2 = StringVar()
    self.label_str2.set("filename 2.db/txt")
    
    self.label_str3 = StringVar()
    self.label_str3.set("Outputfile.db")
    
    self.createLabel(parent=self.master, col=1, row=0, variable=self.label_str1)
    self.createLabel(parent=self.master, col=1, row=1, variable=self.label_str2)
    self.createLabel(parent=self.master, col=3, row=1, variable=self.label_str3, sticky=N)
    
    self.createLabel(parent=parent, label="Output File :", col=3, row=0, sticky=S)
    
    self.createButton(parent=parent, label="Create & Join DB", command=self.createjoin, col=0, row=3, padx=20, pady=20, bd=3)    
    self.createButton(parent=parent, label="    Join DB     ", command=self.join, col=1, row=3, padx=20, pady=20, bd=3)
    self.createButton(parent=parent, label="View O/P db file", command=self.viewdb, col=2, row=3, padx=20, pady=20, bd=3)
    self.createButton(parent=parent, label="     Quit       ", command=self.quit, col=3, row=3, padx=20, pady=20, bd=3)
    
    self.scrollbar = Scrollbar(parent)
    self.scrollbar.grid(column=5, row=0, sticky=E)
    self.sensorListbox = Listbox(parent, height=5, width=17, yscrollcommand=self.scrollbar.set)
    self.sensorListbox.grid(column=5, row=0)
    self.scrollbar.configure(command=self.sensorListbox.yview)
    
    
    self.createButton(parent=parent, label="Select DB", command=self.getDB, col=5, row=1)
    self.createButton(parent=parent, label="Plot Sensor Data", command=self.viewPlot, col=5, row=3, padx=20, pady=20, bd=3)
    
    self.whichSensor = StringVar()
    Radiobutton(parent, text="Vanadium", variable=self.whichSensor, value="-v").grid(column=2, row=0, sticky=SW)
    Radiobutton(parent, text="Cobalt", variable=self.whichSensor, value="-c").grid(column=2, row=1, sticky=NW)
    
    
    #self.progressbar = ttk.Progressbar(self.master, orient=HORIZONTAL, length=200, mode='indeterminate')
    #self.progressbar.grid(column=0, row=4)
    
  def createLabel(self, parent, col, row, font=None, variable=None, label=None, padx=None, pady=None, columnspan=None, rowspan=None, sticky=None):
    if variable==None:
      l = Label(parent, text=label, relief=GROOVE, width=10, font=None)
      l.grid(column=col, row=row, padx=padx, pady=pady, columnspan=columnspan, rowspan=rowspan, sticky=sticky)
    else:
      l = Label(parent, relief=RIDGE, textvariable=variable, width=15, font=None)
      l.grid(column=col, row=row, padx=padx, pady=pady, columnspan=columnspan, rowspan=rowspan, sticky=sticky)
    
  def createButton(self, parent, col, row, label, command, padx=None, pady=None, width=None, bd=None):
    b = Button(parent, text=label, command=command, relief=RAISED, cursor='hand2', width=width, bd=bd)
    b.grid(column=col, row=row, padx=padx, pady=pady)
    
  def createjoin(self):
    self.opt = "--createjoin"
    self.compute()
    
  def join(self):
    self.opt = "--join"
    self.compute()
    
  def quit(self, event=None):
    self.master.quit()
    
  def openfile1(self):
    self.filename1 = askopenfilename(**self.file_opt)
    print(self.filename1)
    if self.filename1 != () and self.filename1 != "":
      self.label_str1.set(os.path.split(self.filename1)[1])
    
  def openfile2(self):
    self.filename2 = askopenfilename(**self.file_opt)
    print(self.filename2)
    if self.filename2 != () and self.filename2 != "":
      self.label_str2.set(os.path.split(self.filename2)[1])
  
  def getDB(self):
    dbName = askopenfilename(**self.file_opt_DB)
    if dbName != () and dbName != "":
      self.databaseName = dbName
      self.sensorNames = get_columnNames(self.databaseName)
      self.sensorListbox.delete(0, END)
      for item in self.sensorNames:
        self.sensorListbox.insert(END, item)
  
  def viewPlot(self):
    operation = ["python3.2", "main.py", "--plot"]
    operation.append(self.databaseName)
    operation.append(self.sensorNames[int( self.sensorListbox.curselection()[0] )])
    subprocess.call(operation)
      
  def viewdb(self):
    subprocess.call(["sqlitebrowser", "{}".format(os.path.join(os.path.split(self.filename1)[0], self.label_str3.get())) ])
  
  def start_stop_bar(self, op):
    if op == 'start':
      self.progressbar.start(10)
    else:
      self.progressbar.stop()
  
  def compute(self):
    operation = ["python3.2", "main.py"]
    operation.append(self.whichSensor.get())
    operation.append(self.opt)
    operation.append(self.filename1)
    operation.append(self.filename2)
    subprocess.call(operation)
    self.databaseName3 = join_database_name(create_database_name(self.label_str1.get()), create_database_name(self.label_str2.get()))
    self.label_str3.set(self.databaseName3)
    
if __name__ == "__main__":
  root = Tk()
  root.geometry("850x250+400+100")
  app = GUI(root)
  root.mainloop()