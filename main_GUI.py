from tkinter import *
from tkinter.filedialog import *
from name_creator import create_database_name, join_database_name
import os
import subprocess


class GUI():
  
  file_opt = {}
  opt = []
  row_counter = 0
  filename1 = ""
  filename2 = ""
  
  def __init__(self, parent):
    self.master = parent
    self.master.title("DBCreator")
    
    self.file_opt['defaultextension'] = '.txt'
    self.file_opt['filetypes'] = [('text files', '.txt'), ('db files', '.db')]
    self.file_opt['parent'] = self.master
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
    self.createLabel(parent=self.master, col=3, row=0, variable=self.label_str3, rowspan=2, sticky=W)
    
    self.createLabel(parent=parent, label="Output File :", col=2, row=0, rowspan=2, sticky=E)
    
    self.createButton(parent=parent, label="Create & Join DB", command=self.createjoin, col=0, row=3, padx=20, pady=20, bd=3)    
    self.createButton(parent=parent, label="    Join DB     ", command=self.join, col=1, row=3, padx=20, pady=20, bd=3)
    self.createButton(parent=parent, label="View O/P db file", command=self.viewdb, col=2, row=3, padx=20, pady=20, bd=3)
    self.createButton(parent=parent, label="     Quit       ", command=self.quit, col=3, row=3, padx=20, pady=20, bd=3)
    
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
    self.opt.append("--createjoin")
    self.compute()
    
  def join(self):
    self.opt.append("--join")
    self.compute()
    
  def quit(self, event=None):
    self.master.quit()
    
  def openfile1(self):
    self.filename1 = askopenfilename(**self.file_opt)
    if self.filename1 != ():
      self.label_str1.set(os.path.split(self.filename1)[1])
    
  def openfile2(self):
    self.filename2 = askopenfilename(**self.file_opt)
    if self.filename2 != ():
      self.label_str2.set(os.path.split(self.filename2)[1])
    
  def viewdb(self):
    subprocess.call(["sqlitebrowser", "{}".format(os.path.join(os.path.split(self.filename1)[0], self.label_str3.get())) ])
        
  def compute(self):
    operation = ["python3.2", "main.py"] + self.opt
    operation.append(self.filename1)
    operation.append(self.filename2)
    subprocess.call(operation)
    self.databaseName3 = join_database_name(create_database_name(self.label_str1.get()), create_database_name(self.label_str2.get()))
    self.label_str3.set(self.databaseName3)
    
if __name__ == "__main__":
  root = Tk()
  root.geometry("650x200+400+100")
  app = GUI(root)
  root.mainloop()