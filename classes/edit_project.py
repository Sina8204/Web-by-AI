import tkinter as tk
from tkinter import ttk
import sys , os
import json
import re
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__) , '..' , 'classes')))
from file_explorer_class import open_fileExplorer
from api_class import models
from web_runner_class import WebRunner

py_3_9 = r"D:\Apps\Python\installed\3.9\python.exe"

webruner = WebRunner()
fe = open_fileExplorer()
model_html_editor = models()
instruction_system = {
    'html':(
        "You are an AI model specialized in editing HTML, CSS, and JavaScript code based on user-specified modifications."
        "Your input consists of two parts:"
        "1. A block of HTML code that references external CSS and JS files by name."
        "2. A list of changes that should be applied to the HTML, CSS, and JS code."
        "Instructions:"
        "- Apply the changes exactly as described by the user."
        "- Output the final code for each file separately: one for HTML, one for CSS, and one for JavaScript."
        '- Use the filenames referenced in the HTML (e.g., href="style.css", src="script.js") to determine which CSS and JS files to modify.'
        "- Do not embed CSS or JavaScript inside the HTML file."
        "- Do not include any explanations, comments, or extra text before or after the code."
        "- Do not include any code from other programming languages."
        "- Wrap each code block in its appropriate Markdown syntax:"
        "- HTML code: ```html"
        "- CSS code: ```css"
        "- JavaScript code: ```javascript"
        "- Ensure each file’s content is clean, valid, and executable."


    ) ,
    'css' :(
        "You are an AI model specialized in editing CSS code based on user-specified style changes."
        "Your input consists of two parts:"
        "1. A block of CSS code that serves as the base."
        "2. A list of style changes that should be applied to this CSS."
        "Instructions:"
        "- Apply the changes exactly as described by the user."
        "- Output only the final CSS code."
        "- Do not include any HTML, JavaScript, or other programming languages."
        "- Do not include any explanations, comments, or extra text before or after the code."
        "- Ensure the CSS is clean, valid, and executable."
    ) ,
    'js' : (
        "You are an AI model specialized in editing JavaScript code based on user-specified modifications."
        "Your input consists of two parts:"
        "1. A block of JavaScript code that serves as the base."
        "2. A list of changes that should be applied to this code."
        "Instructions:"
        "- Apply the changes exactly as described by the user."
        "- Output only the final JavaScript code."
        "- Do not include any HTML, CSS, or other programming languages."
        "- Do not include any explanations, comments, or extra text before or after the code."
        "- Ensure the JavaScript code is clean, valid, and executable."
    )
}

def save_code_blocks(model_output: str , path_html , path_css , path_js , mode):
    # مسیر فایل‌ها
    html_path = path_html
    css_path = path_css
    js_path = path_js

    # استخراج کدها با استفاده از تگ‌های markdown
    html_code = extract_code_by_language(model_output, "html")
    css_code = extract_code_by_language(model_output, "css")
    js_code = extract_code_by_language(model_output, "javascript")

    # ذخیره‌سازی در فایل‌ها
    if mode == 'html':
        with open(html_path, "w", encoding="utf-8") as f_html:
            f_html.write(html_code)

        with open(css_path, "w", encoding="utf-8") as f_css:
            f_css.write(css_code)

        with open(js_path, "w", encoding="utf-8") as f_js:
            f_js.write(js_code)
    elif mode == 'css':
        with open(css_path, "w", encoding="utf-8") as f_css:
            f_css.write(css_code)
    elif mode == "js":
        with open(js_path, "w", encoding="utf-8") as f_js:
            f_js.write(js_code)
    else :
        print("Warning : Invalid mode !!!")

    print("✅ فایل‌ها با موفقیت ذخیره شدند.")

def extract_code_by_language(text: str, language: str) -> str:
    """
    استخراج کد از بلوک markdown با زبان مشخص‌شده (html, css, javascript)
    """
    pattern = rf"```{language}\n(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""

def send_edit_html_requiest(key , mode , prompt , html_path , css_path , js_path):
    model_html_editor.key = key
    model_html_editor.system_instruction = instruction_system["html"]
    model_html_editor.user_input = prompt
    model_html_editor.send_requiest_to_model()
    print(f"rispons : \n{model_html_editor.outpute()}")
    save_code_blocks(model_html_editor.outpute() , html_path , css_path , js_path , mode)

class codes_and_scripts:
    def __init__(self , root):
        self.root = root

        # تنظیم کشسانی برای root
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=2)

        # فریم جزئیات پروژه
        self.frame_project_details = tk.Frame(self.root)
        self.frame_project_details.grid(row=0 , column=0 , sticky="ew")
        self.frame_project_details.columnconfigure(0 , weight=1)
        self.frame_project_details.columnconfigure(1 , weight=1)

        # فریم ابزار های پروژه
        self.frame_project_tools = tk.Frame(self.root)
        self.frame_project_tools.grid(row=1 , column=0 , sticky="ew")
        self.frame_project_tools.columnconfigure(0 , weight=1)
        self.frame_project_tools.columnconfigure(1 , weight=1)

        # فریم کدها و اسکریپت‌ها
        self.frame_codes_and_scripts = tk.Frame(self.root)
        self.frame_codes_and_scripts.grid(row=2 , column=0 , sticky="nsew")  # کشسانی کامل
        self.frame_codes_and_scripts.columnconfigure(0 , weight=1)
        self.frame_codes_and_scripts.rowconfigure(0 , weight=1)  # ردیف کشسان

        #++++++++++++++++++++++++ <project details frame widgets> +++++++++++++++++++++++
        self.button_import_project = tk.Button(self.frame_project_details , text='Import')
        self.entry_project_path = tk.Entry(self.frame_project_details , font=("Arial" , 14) , width=70 , state='readonly')

        self.button_import_project.grid(row=0 , column=0 , padx=10 , sticky="ew")
        self.entry_project_path.grid(row=0 , column=1 , sticky="ew")

        #++++++++++++++++++++++++ <project tools frame widgets> +++++++++++++++++++++++
        self.entry_opened_file = tk.Entry(self.frame_project_tools , state='readonly')
        self.button_save_file = tk.Button(self.frame_project_tools , text='Save' , command=self.save_opened_file)
        self.button_run_project = tk.Button(self.frame_project_tools ,
                                        text='Run' ,
                                        command=(lambda : webruner.open_with_default_browser(fe.open_temp_file()['html_path']))
                                        )

        self.entry_opened_file.grid(row=0 , column=0 , columnspan=2 , sticky="ew")
        self.button_save_file.grid(row=1 , column=0 , sticky="ew")
        self.button_run_project.grid(row=1 , column=1 , sticky="ew")

        #++++++++++++++++++++++++ <codes and scripts frame widgets> +++++++++++++++++++++
        self.textBox_codes = tk.Text(self.frame_codes_and_scripts , height=27)
        self.textBox_codes.grid(row=0 , column=0 , pady=10 , sticky="nsew")  # کشش کامل در فریم

    def save_opened_file(self):
        with open(self.entry_opened_file.get() , 'w+' , encoding='utf-8') as file:
            file.write(self.textBox_codes.get("1.0" , tk.END))

class project_manager:
    def __init__(self , root , detaile : codes_and_scripts):
        self.root = root
        self.detail = detaile
        self.tree = ttk.Treeview(self.root)
        self.tree.pack(fill=tk.BOTH , expand=True)
        self.detail.button_import_project.config(command=self.load_project)
        self.tree.bind("<Double-1>", self.on_item_double_click)  # اتصال رویداد کلیک
    
    def load_project(self):
        path = fe.open_folder()
        detailes = {}
        if os.path.exists(f"{path}/details.json"):
            with open(f"{path}/details.json" , 'r+' , encoding='utf-8') as f:
                detailes = json.load(f)
                fe.load_temp_file(detailes)
                print("------------------------------------------")
                print(f"temp : {fe.open_temp_file()}")
                print("------------------------------------------")
            detailes_key_lists = list(detailes.keys())
            if "is_valid" in detailes_key_lists :
                self.detail.entry_project_path.config(state='normal')
                self.detail.entry_project_path.delete(0 , tk.END)
                self.detail.entry_project_path.insert(0 , path)
                self.detail.entry_project_path.config(state='readonly')
                # path = self.detail.entry_project_path.get()
                fe.browse_and_load(path , self.tree)
                print("Load tree is sucssesfully :)")
            else:
                print(f"Warning : Opened invalid folder project\n\tpath{path}/details.json")
        else:
            print(f"Warning : you shuld try open a directory that have details.json file !!!\n\tpath{path}")
    
    def load_new_project(self , html_file_name : str):
        path = self.detail.entry_project_path.get()
        html_file_path = f"{path}/{html_file_name}"
        fe.browse_and_load(path , self.tree)
        print("Load tree is sucssesfully :)")
        self.detail.textBox_codes.delete("1.0", "end")
        if os.path.exists(html_file_path):
            with open (html_file_path , 'r+' , encoding='utf-8') as file:
                self.detail.textBox_codes.insert("1.0" , file.read())
            print("Load tree is sucssesfully :)")
        else :
            print("sorry :(\n\tUnfortunately, a problem has occurred in the construction of your website.")
            print(f"Because html file in '{path}' isn't created")
            print("check your directory. if the html file created with some other names ,")
            print("you can import that in edit tab :)")

    def on_item_double_click(self, event):
        selected_item = self.tree.focus()
        item_text = self.tree.item(selected_item, "text")
        if item_text:
            path = f"{self.detail.entry_project_path.get()}/{item_text}"
            if os.path.exists(path):
                with open(path , 'r+' , encoding='utf-8') as file:
                    self.detail.textBox_codes.delete("1.0", "end")
                    self.detail.textBox_codes.insert("1.0" , file.read())
                self.detail.entry_opened_file.config(state='normal')
                self.detail.entry_opened_file.delete(0 , tk.END)
                self.detail.entry_opened_file.insert(0 , path)
                self.detail.entry_opened_file.config(state='readonly')
                print(f"{path} imported to code text box")
            else:
                print(f"Warning : There isn't file in directory '{path}' !!!")
        else:
            print("⚠️ آیتمی انتخاب نشده یا نامی ندارد.")


class ai_editor:
    def __init__(self , root , codes_and_script : codes_and_scripts):
        self.root = root
        self.codes_and_script = codes_and_script
        # frame send promt and edit modes
        self.frame_editing_options = tk.Frame(self.root)
        self.frame_editing_options.pack(expand=True)

        # frame promt text box
        self.frame_textBox_promt = tk.Frame(self.root)
        self.frame_textBox_promt.pack(fill=tk.BOTH , padx=5 , pady=10 , expand=True)

        #++++++++++++++++++++++++ <send promt and edit modes frame widgets> +++++++++++++++++++++++
        self.mode = tk.StringVar(value='html')
        self.radioButton_html = tk.Radiobutton(self.frame_editing_options , text='HTML' , variable=self.mode , value='html')
        self.radioButton_css = tk.Radiobutton(self.frame_editing_options , text='CSS' , variable=self.mode , value='css')
        self.radioButton_js = tk.Radiobutton(self.frame_editing_options , text='Java Script' , variable=self.mode , value='js')
        
        self.button_send = tk.Button(self.frame_editing_options , text='Send' , command= self.send_prompt_requiest)

        self.radioButton_html.pack(padx=10 , expand=True , side="left")
        self.radioButton_css.pack(padx=10 , expand=True , side="left")
        self.radioButton_js.pack(padx=10 , expand=True , side="left")
        self.button_send.pack(padx=10 , expand=True)

        #++++++++++++++++++++++++ <promt text box frame widgets> +++++++++++++++++++++
        self.textBox_edit_promt = tk.Text(self.frame_textBox_promt)
        self.textBox_edit_promt.pack(fill=tk.BOTH , expand=True)
    
    def send_prompt_requiest(self):
        project_path = self.codes_and_script.entry_project_path.get()
        mode = self.mode.get()
        details = {}
        line = "----------------------------------------------"
        print(f"details path : {project_path}/details.json")
        with open(f"{project_path}/details.json" , "r+" , encoding='utf-8') as f:
            details = json.load(f)
        html_path = details['html_path']
        css_path = details['css_path']
        js_path = details['js_path']

        if mode == 'html':
            with open(html_path, 'r+', encoding='utf-8') as html_file:
                html_code = html_file.read()
            with open(css_path, 'r+', encoding='utf-8') as css_file:
                css_code = css_file.read()
            with open(js_path, 'r+', encoding='utf-8') as js_file:
                js_code = js_file.read()

            prompt = f"html code :\n{html_code}\n\ncss code :\n{css_code}\n\njava script cod :\n{js_code}\n\n{line}\n{self.textBox_edit_promt.get('1.0', tk.END)}"

            send_edit_html_requiest(
                details['api_key'],
                mode,
                prompt,
                html_path,
                css_path,
                js_path
            )
            print('send html requist')
        elif (mode == 'css'):
            with open(css_path , 'r+' , encoding='utf-8') as css_file:
                send_edit_html_requiest(
                            details['api_key'] ,
                            mode ,
                            f"css code :\n{css_file.read()}\n\n{line}\n{self.textBox_edit_promt.get('1.0' , tk.END)}" ,
                            html_path,
                            css_path ,
                            js_path
                        )
            print('send css requiest')
        else:
            with open(js_path , 'r+' , encoding='utf-8') as js_file:
                send_edit_html_requiest(
                            details['api_key'] ,
                            mode ,
                            f"java script cod :\n{js_file.read()}\n\n{line}\n{self.textBox_edit_promt.get('1.0' , tk.END)}" ,
                            html_path,
                            css_path ,
                            js_path
                        )
            print('send js requiest')
        if self.codes_and_script.entry_opened_file.get():
            with open(self.codes_and_script.entry_opened_file.get() , "r+" , encoding='utf-8') as file:
                self.codes_and_script.textBox_codes.delete('1.0' , tk.END)
                self.codes_and_script.textBox_codes.insert('1.0' , file.read())
        elif self.codes_and_script.entry_opened_file.get() == "":
            with open(fe.open_temp_file()['html_path'] , "r+" , encoding='utf-8') as file:
                self.codes_and_script.textBox_codes.delete('1.0' , tk.END)
                self.codes_and_script.textBox_codes.insert('1.0' , file.read())
        else:
            with open(fe.open_temp_file()['html_path'] , "r+" , encoding='utf-8') as file:
                self.codes_and_script.textBox_codes.delete('1.0' , tk.END)
                self.codes_and_script.textBox_codes.insert('1.0' , file.read())

class edit_project_class:
    def __init__(self , root):
        self.root = root
        #++++++++++++++++++++++++ <PandWindows> #++++++++++++++++++++++++
        self.main_pw = tk.PanedWindow(self.root)
        self.main_pw.pack(fill=tk.BOTH , expand=1)

        self.vertical_pw = tk.PanedWindow(self.main_pw , orient=tk.VERTICAL)
        self.pw_top_horizontala = tk.PanedWindow(self.vertical_pw , orient=tk.HORIZONTAL)
        self.pw_down_horizontala = tk.PanedWindow(self.vertical_pw , orient=tk.HORIZONTAL)

        self.main_pw.add(self.vertical_pw)
        self.vertical_pw.add(self.pw_top_horizontala)
        self.vertical_pw.add(self.pw_down_horizontala)

        self.cod_pw = tk.PanedWindow(self.pw_top_horizontala)
        # self.web_pw = tk.PanedWindow(self.pw_top_horizontala)
        self.pw_top_horizontala.add(self.cod_pw)
        # self.pw_top_horizontala.add(self.web_pw)

        self.file_manager_pw = tk.PanedWindow(self.pw_down_horizontala)
        self.ai_editor_pw = tk.PanedWindow(self.pw_down_horizontala)
        self.pw_down_horizontala.add(self.file_manager_pw)
        self.pw_down_horizontala.add(self.ai_editor_pw)
        
        #++++++++++++++++++++++++ <Frames> #++++++++++++++++++++++++
        self.fram_cod = tk.Frame(self.cod_pw , width=750 , height=500)
        # self.fram_web = tk.Frame(self.web_pw)
        self.fram_file_manager = tk.Frame(self.file_manager_pw , width=300)
        self.fram_ai_editor = tk.Frame(self.ai_editor_pw)

        self.cod_pw.add(self.fram_cod)
        # self.web_pw.add(self.fram_web)
        self.file_manager_pw.add(self.fram_file_manager)
        self.ai_editor_pw.add(self.fram_ai_editor)

        self.codes_and_scripts = codes_and_scripts(self.fram_cod)
        self.ai_editor_class = ai_editor(self.fram_ai_editor , self.codes_and_scripts)
        self.file_manager_class = project_manager(self.fram_file_manager , self.codes_and_scripts)

# app = tk.Tk()
# app.title("Edit project")
# app.geometry("1280x720")

# edit_project_class(app)

# app.mainloop()