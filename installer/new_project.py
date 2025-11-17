import sys , os
import tkinter as tk
from tkinter import ttk
from google import genai
from tkinter import messagebox
import re
import json
import threading

from file_explorer_class import open_fileExplorer
from api_class import models
from edit_project import edit_project_class
from operator_and_waiting_class import wait

fe = open_fileExplorer()
model_web_creator = models()
# client = genai.Client(api_key="AIzaSyALhLOtosNenar3KFvEpmFrA2n7TAavxqY")
placeholder_text = "Enter your idea :)\nWhat kind of site do you want to build?\nJust write to me what's on your mind ;)"
placeholder_entry = "Enter your api key..."
def save_code_blocks(model_output: str, project_name: str, output_dir: str = "."):
    # مسیر فایل‌ها
    html_path = os.path.join(output_dir, f"{project_name}_html_cod.html")
    css_path = os.path.join(output_dir, f"{project_name}_css_cod.css")
    js_path = os.path.join(output_dir, f"{project_name}_js_code.js")

    # استخراج کدها با استفاده از تگ‌های markdown
    html_code = extract_code_by_language(model_output, "html")
    css_code = extract_code_by_language(model_output, "css")
    js_code = extract_code_by_language(model_output, "javascript")

    # ذخیره‌سازی در فایل‌ها
    with open(html_path, "w", encoding="utf-8") as f_html:
        f_html.write(html_code)

    with open(css_path, "w", encoding="utf-8") as f_css:
        f_css.write(css_code)

    with open(js_path, "w", encoding="utf-8") as f_js:
        f_js.write(js_code)

    print("✅ فایل‌ها با موفقیت ذخیره شدند.")

def extract_code_by_language(text: str, language: str) -> str:
    """
    استخراج کد از بلوک markdown با زبان مشخص‌شده (html, css, javascript)
    """
    pattern = rf"```{language}\n(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""

class new_project_class():
    def __init__(self , root , edit_project : edit_project_class , notebook : ttk.Notebook):
        self.root = root
        self.wait = wait(self.root)
        self.edit_project = edit_project
        self.notebook = notebook
        self.json_dtails = {}
        # self.title("New project")
        # self.geometry("1280x720")

        self.frame_front = tk.Frame(self.root)
        self.frame_project_name = tk.Frame(self.frame_front)
        self.frame_api_key = tk.Frame(self.frame_front)
        self.button_creat_project = tk.Button(self.frame_front , text="Create new project" , command=self.create_website)
        #####################frame_project_name widgets##########################
        self.Label_project_name = tk.Label(self.frame_project_name , text="Project name :" , font=("Arial" , 14))
        self.entry_project_name = tk.Entry(self.frame_project_name , font=("Arial" , 14))
        self.Label_project_name.pack(side="left")
        self.entry_project_name.pack(padx=5)
        #####################frame_project_name widgets##########################

        #####################frame_api_key widgets##########################
        self.button_open_file_api_key = tk.Button(self.frame_api_key , text="Open a file" , command=self.open_api_key_file_text)
        self.entry_api_key = tk.Entry(self.frame_api_key , fg='gray' , width=25 , font=("Arial" , 14))
        self.entry_api_key.insert(0 , placeholder_entry)
        self.button_open_file_api_key.pack(side="left")
        self.entry_api_key.pack(padx=5)

        self.entry_api_key.bind("<FocusIn>", self.on_api_key_entry_on_focus_in)
        self.entry_api_key.bind("<FocusOut>", self.on_api_key_entry_on_focus_out)
        #####################frame_api_key widgets##########################
        
        self.textBox_project_comments = tk.Text(self.frame_front , fg="grey")
        self.textBox_project_comments.insert("1.0", placeholder_text)
        self.textBox_project_comments.bind("<FocusIn>", self.on_promt_textBox_on_focus_in)
        self.textBox_project_comments.bind("<FocusOut>", self.on_promt_textBox_on_focus_out)

        self.button_creat_project.pack(pady=10)
        self.frame_project_name.pack(pady=10) #pack frame_project_name
        self.frame_api_key.pack(pady=10)
        self.textBox_project_comments.pack()
        self.frame_front.pack(expand=True)
        

    
    def switch_to_tab(self , index):
        self.notebook.select(index)  # تغییر تب با ایندکس

    def open_folder(self):
        try :
            directory = fe.open_folder()
            return directory
        except Exception as e:
            print (f"Error : {e}")
    
    def creat_jsonFile_for_project(self):
        fe.creat_dictionary_for_project()

    def create_website(self):
        project_path = fe.open_folder()
        sys_instruction = (
            "Only output code."
            "Do not include any explanations, comments, or extra text."
            f"Write HTML code as if it will be placed in a file named {self.entry_project_name.get()}_html_cod.html."
            f"Write CSS code as if it will be placed in a file named {self.entry_project_name.get()}_css_cod.css."
            f"Write JavaScript code as if it will be placed in a file named {self.entry_project_name.get()}_js_code.js. "
            "In the HTML code, correctly link to css_cod.css using a <link> tag and to js_code.js using a <script> tag."
            "Only output the code. No additional text or description."
        )
        model_web_creator.key = self.entry_api_key.get()
        if (not model_web_creator.key):
            messagebox.showerror(title="Error : Invalid api key" , message="You should enter your api key and it must be valid api key")
            print(f"Warning : You shuld enter a api key at the its Entry!!!")
            return
        print(f"API key : {model_web_creator.key}")
        
        model_web_creator.system_instruction = sys_instruction
        print(f"system instruction : {model_web_creator.system_instruction}")

        model_web_creator.user_input = self.textBox_project_comments.get("1.0", "end")
        if (not model_web_creator.user_input):
            messagebox.showerror(title="Error : Invalid project name" , message="You should enter a name for your project")
            print(f"Warning : You shuld enter a promt at the text box")
            return
        print(f"your idea : {model_web_creator.user_input}")

        if self.textBox_project_comments.get("1.0" , "end-1c") == "" or self.textBox_project_comments.get("1.0" , "end-1c") == placeholder_text:
            messagebox.showerror(title="Error : Invalid promt :|" , message="You should enter a promt")
            print(f"Warning : You shuld enter a promt at the text box")
            return
        try :
            model_web_creator.send_requiest_to_model()
            print(f"Your code : \n {model_web_creator.outpute()}")
            save_code_blocks(model_web_creator.outpute() , self.entry_project_name.get() , project_path)
            
            self.json_details = fe.creat_dictionary_for_project(project_path , self.entry_project_name.get())
            self.json_details.update({'api_key' : model_web_creator.key})
            fe.load_temp_file(self.json_details)
            print(f"temp : {fe.open_temp_file()}")
            print(f"-------------------------------------\n")
            print(f"project path : {project_path}\n")
            print(f"name : {self.entry_project_name.get()}\n")

            with open(f"{project_path}/details.json" , 'w+' , encoding="utf-8") as f:
                json.dump(self.json_details , f , ensure_ascii=False, indent=2)
            entry_project_path = self.edit_project.codes_and_scripts.entry_project_path
            entry_project_path.config(state='normal')
            entry_project_path.delete(0 , tk.END)
            entry_project_path.insert(0 , project_path)
            entry_project_path.config(state='readonly')
            self.switch_to_tab(1)
            self.edit_project.file_manager_class.load_new_project(f"{self.entry_project_name.get()}_html_cod.html")
            
        except Exception as e:
            print(f"Error : {e}")
    
    def open_api_key_file_text(self):
        file_path = fe.open_file()
        api_key = ""
        if os.path.exists(file_path):
            with open(file_path , 'r' , encoding='utf-8') as f:
                api_key = f.read()
            self.entry_api_key.config(fg="black" , show='*')
            self.entry_api_key.delete(0 , tk.END)
            self.entry_api_key.insert(0 , api_key)
            print(f"API key : {model_web_creator.key}")
        else:
            print ("Warning : Invalid api key file !!!")

    def on_promt_textBox_on_focus_in(self , event):
        if self.textBox_project_comments.get("1.0" , "end-1c") == placeholder_text:
            self.textBox_project_comments.delete("1.0" , "end")
            self.textBox_project_comments.config(fg="black")  # رنگ متن کاربر
    
    def on_api_key_entry_on_focus_in(self , event):
        if self.entry_api_key.get() == placeholder_entry:
            self.entry_api_key.delete(0 , tk.END)
            self.entry_api_key.config(fg="black" , show='*')  # رنگ متن کاربر

    def on_promt_textBox_on_focus_out(self , event):
        if self.textBox_project_comments.get("1.0" , "end-1c") == "" :
            self.textBox_project_comments.insert("1.0", placeholder_text)
            self.textBox_project_comments.config(fg="grey")  # رنگ placeholder
    
    def on_api_key_entry_on_focus_out(self , event):
        if self.entry_api_key.get() == "" :
            self.entry_api_key.insert(0, placeholder_entry)
            self.entry_api_key.config(fg="grey" , show='')  # رنگ placeholder

# test = new_project_class()
# test.mainloop()






# # دریافت ورودی از کاربر
        # user_input = self.textBox_project_comments.get("1.0", "end")

        # # ارسال درخواست به مدل
        # response = client.models.generate_content(
        #     model="gemini-2.5-flash",
        #     config=genai.types.GenerateContentConfig(system_instruction=sys_instruction),
        #     contents=user_input
        # )
        #print(f"Your code : \n {response.text}")