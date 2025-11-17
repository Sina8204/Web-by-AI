import os , sys
from tkinter import filedialog as fd
import os , sys
from tkinter import filedialog as fd
from tkinter import ttk
import json
from pathlib import Path

class open_fileExplorer:
    def __init__(self):
        pass

    def open_folder(self , Titel = "Select a folder"):
        return fd.askdirectory(title=Titel)
    
    def open_file(self , Titel = "Select a file" , mode = False):
        if mode:
            return fd.askopenfilenames(title=Titel)
        else :
            return fd.askopenfilename(title=Titel)

    def creat_dictionary_for_project(self , path , name):
        return {
            "is_valid" : True ,
            "project_path" : path ,
            "html_path" : f"{path}/{name}_html_cod.html" , 
            "css_path" : f"{path}/{name}_css_cod.css" , 
            "js_path" : f"{path}/{name}_js_code.js" 
        }
    
    def populate_treeview(self , tree : ttk.Treeview , parent, path):
        try:
            for item in os.listdir(path):
                abs_path = os.path.join(path, item)
                node_id = tree.insert(parent, 'end', text=item, open=False)
                if os.path.isdir(abs_path):
                    self.populate_treeview(tree, node_id, abs_path)
        except PermissionError:
            pass  # Skip folders without permission

    def browse_and_load(self , path , tree : ttk.Treeview):
        if path:
            tree.delete(*tree.get_children())
            self.populate_treeview(tree, '', path)
    
    def open_temp_file(self):
        with open("temp.json" , 'r+' , encoding='utf-8') as f:
            return json.load(f)
    
    def load_temp_file(self , items):
        with open("temp.json" , 'w+' , encoding='utf-8') as f:
            json.dump(items , f , ensure_ascii=False , indent=2)
    
    def reset_temp_file(self):
        with open("temp.json" , 'w+' , encoding='utf-8') as f:
            f.write("")

    # def check_folder_empty(self , folder_path):
    #     try:
    #         path = Path(folder_path)
            
    #         if not path.exists():
    #             raise FileNotFoundError(f"پوشه '{folder_path}' وجود ندارد")
            
    #         if not path.is_dir():
    #             raise NotADirectoryError(f"'{folder_path}' یک پوشه نیست")
            
    #         # بررسی وجود آیتم‌های قابل مشاهده
    #         items = list(path.iterdir())
    #         visible_items = [item for item in items if not item.name.startswith('.')]
            
    #         return len(visible_items) == 0, len(visible_items)
            
    #     except Exception as e:
    #         return False, f"خطا: {e}"


    # def build_tree(self , tree : ttk.Treeview , parent, path):
    #     try:
    #         items = sorted(os.listdir(path))
    #         for item in items:
    #             full_path = os.path.join(path, item)
    #             display_name = f"📁 {item}" if os.path.isdir(full_path) else f"📄 {item}"
    #             node = tree.insert(parent, 'end', text=display_name, values=[full_path])
    #             if os.path.isdir(full_path):
    #                 self.build_tree(tree, node, full_path)
    #     except PermissionError:
    #         pass
    
    # def import_templates_to_manager(self,tree, data):
    #     nodes = {}
    #     for key, item in data.items():
    #         parent = item["parent"]
    #         label = key  # استفاده از کلید به عنوان نام آیتم
    #         if parent == "":
    #             nodes[key] = tree.insert("", "end", iid=key, text=label)
    #         else:
    #             nodes[key] = tree.insert(parent, "end", iid=key, text=label)

    # def add_tree(self , tree : ttk.Treeview , path):
    #     folder_path = path
    #     if folder_path:
    #         tree.delete(*tree.get_children())
    #         root_name = os.path.basename(folder_path)
    #         root_node = tree.insert('', 'end', text=f"📁 {root_name}", values=[folder_path], open=True)
    #         self.build_tree(tree, root_node, folder_path)

    # def clear_pathes(self):
    #     if os.path.exists(self.file_path):
    #         with open (self.file_path , "w+" , encoding='utf-8') as f:
    #             f.write("")
    
    # def extract_file_names_of_path(self , path : str):
    #     path = Path(path)
    #     file_names = [f.name.split('.')[0] for f in path.iterdir() if f.is_file()]
    #     return file_names
    
    # def delete_file(self, path: str, target_stem: str):
    #     path = Path(path)
    #     for f in path.iterdir():
    #         if f.is_file() and f.stem == target_stem:
    #             f.unlink()
    #             print(f"فایل '{f.name}' حذف شد.")
    #             return
    #     print(f"فایلی با نام '{target_stem}' پیدا نشد.")