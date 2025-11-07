import webbrowser as wb
import tkinter as tk
from tkinter import messagebox
import platform
import sys , os , json

import threading

class WebRunner():
    def __init__(self):
        pass
    def open_with_default_browser(self , path):
        if path:
            if path.lower().endswith(".html"):
                wb.open(f"file://{os.path.abspath(path)}")
            else:
                messagebox.showerror("Error !!! \npleas run just .html files")
    
    def open_with_other_browser(self , browser_path , html_path):
        if browser_path:
            if html_path:
                if html_path.lower().endswith(".html"):
                    wb.get(browser_path).open(f"file://{os.path.abspath(html_path)}")
                else:
                    messagebox.showerror("Error !!! \npleas run just .html files")
            else:
                messagebox.showerror(f"Error : Invalid html path '{html_path}'\nPleas enter html file path")
        else:
            messagebox.showerror(f"Error : Invalid browser path '{browser_path}'\nPleas enter true browser path")



# from cefpython3 import cefpython as cef
#from edit_project import codes_and_scripts as cas
# class WebRunner:
#     def __init__(self, root , path : cas):
#         self.root = root
#         self.path = path.entry_project_path
#         self.frame_web_button_tools = tk.Frame(self.root)
#         self.frame_web_button_tools.pack(side="top", fill=tk.X)

#         self.button_refresh = tk.Button(
#             self.frame_web_button_tools,
#             text='Refresh'
#         )
#         self.button_refresh.pack(side="left" , fill=tk.BOTH , padx=5, pady=5 , expand=True)

#         self.frame = tk.Frame(self.root)
#         self.frame.pack(fill=tk.BOTH, expand=True)