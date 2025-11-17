import sys , os
import tkinter as tk
from tkinter import ttk
import json

from new_project import new_project_class
from edit_project import edit_project_class

class web_by_ai(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Web by ai")
        self.geometry("1280x720")
        #set style for notebook
        style = ttk.Style(self)
        style.theme_use('default')
        style.configure('TNotebook.Tab', anchor='center', padding=[20, 10])
        #creat notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.new_project = tk.Frame(self.notebook)
        self.edit_project = tk.Frame(self.notebook)

        self.edit_project_class = edit_project_class(self.edit_project)
        self.new_project_class = new_project_class(self.new_project , self.edit_project_class , self.notebook)
        

        self.notebook.add(self.new_project ,text= "Start")
        self.notebook.add(self.edit_project ,text= "Edit")

app = web_by_ai()
app.mainloop()
