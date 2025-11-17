import tkinter as tk
import threading
import time
import tkinter as tk
import sys , os
import json
from tkinter import messagebox

from api_class import models

operator_model = models()
def send_requiest(key , prompt):
    operator_model.key = key
    operator_model.system_instruction = (
        "You are an assistant specialized ONLY in HTML, CSS, and JavaScript.",
        "Your tasks are:",
        "1. If the user provides HTML, CSS, or JavaScript code, analyze it carefully.",
        "- Help fix bugs and errors.",
        "- Suggest improvements, new features, or additional elements.",
        "- Explain your reasoning clearly and step by step.",
        "2. If the user does NOT provide code, you must write example HTML, CSS, and JavaScript code yourself, based on the user’s request.",
        "- Always keep the code modular, clean, and easy to understand.",
        "- Provide explanations alongside the code.",
        "3. You MUST restrict your guidance to HTML, CSS, and JavaScript only.",
        "- If the user asks about other topics (e.g., Python, databases, or non-programming subjects), politely respond:",
            '"I am only specialized in HTML, CSS, and JavaScript."',
        "4. Always encourage best practices:",
        "- Semantic HTML structure.",
        "- Responsive CSS design.",
        "- Efficient and readable JavaScript.",
        "5. Communicate in a clear, helpful, and educational tone.",
        "6. Always respond in the same language the user writes in.",
        "- Detect the user’s input language automatically.",
        "- Respond in that language, whether it is Persian, English, French, Spanish, Arabic, Chinese, or any other.",
        "- Do not switch languages unless the user explicitly asks."
    )
    operator_model.user_input = prompt
    operator_model.send_requiest_to_model()
    print(f"rispons : \n{operator_model.outpute()}")
    return operator_model.outpute()

class wait:
    def __init__(self, root):
        self.root = root
        self.loading_win = None

    def waiting(self):
        self.loading_win = tk.Toplevel(self.root)
        self.loading_win.title("Please Wait")
        self.loading_win.geometry("200x100")
        tk.Label(self.loading_win, text="Loading... Please wait").pack(expand=True)

    def end_wait(self):
        if self.loading_win and self.loading_win.winfo_exists():
            self.loading_win.destroy()
            self.loading_win = None

class ChatWindow:
    def __init__(self, root):
        self.root = root
        self.wait = wait(self.root)
        self.promt_saver = ""
        # self.root.title("Chat Window")

        # ساخت Canvas و Scrollbar
        self.canvas = tk.Canvas(root, width=400, height=300, bg="white")
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # اتصال اسکرول
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # ساخت Frame داخل Canvas
        self.message_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.message_frame, anchor="nw")

        # تنظیم اسکرول هنگام تغییر اندازه
        self.message_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # فعال‌سازی اسکرول موس
        #self.root.bind_all("<MouseWheel>", self._on_mousewheel)

        # فعال‌سازی اسکرول موس روی کل برنامه
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)   # ویندوز/مک
        self.root.bind_all("<Button-4>", self._on_mousewheel)     # لینوکس بالا
        self.root.bind_all("<Button-5>", self._on_mousewheel)     # لینوکس پایین

        # ورودی و دکمه ارسال
        self.entry = tk.Entry(root, width=40)
        self.entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.send_button = tk.Button(root, text="ارسال", command= self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=5)

    def _on_mousewheel(self, event):
        """اسکرول موس روی canvas حتی وقتی موس روی message_frame یا ویجت‌های داخلشه"""
        bbox = self.canvas.bbox("all")
        if not bbox:
            return

        content_height = bbox[3] - bbox[1]
        canvas_height = self.canvas.winfo_height()

        if content_height <= canvas_height:
            return

        # ویندوز/مک
        if event.delta:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        # لینوکس
        elif event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")

    def send_message(self):
        message = self.entry.get().strip()
        self.promt_saver = message
        if message:
            self._add_message(message, sender="user")
            self.entry.delete(0, tk.END)
            # شبیه‌سازی دریافت پاسخ
            threading.Thread(target=self.receive_message , daemon=True).start()

    # def simulate_receive(self):
    #     # نمایش پنجره انتظار
    #     self.root.after(0, self.wait.waiting)
    #     # شبیه‌سازی تأخیر سرور
    #     time.sleep(5)
    #     # افزودن پیام و بستن پنجره در Thread اصلی
    #     self.root.after(0, lambda: self._add_message("سلام! چطور می‌تونم کمکتون کنم؟", sender="operator"))
    #     self.root.after(0, self.wait.end_wait)

    def receive_message(self):
        data = {}
        codes = ""
        try :
            with open("temp.json" , 'r+' , encoding='utf-8') as f:
                data = json.load(f)
            with open(data["html_path"] , 'r+' , encoding='utf-8') as f:
                codes += f"```html \n{f.read()}\n```" 
            with open(data["css_path"] , 'r+' , encoding='utf-8') as f:
                codes += f"```css \n{f.read()}\n```" 
            with open(data["js_path"] , 'r+' , encoding='utf-8') as f:
                codes += f"```Java Script \n{f.read()}\n```" 
        except Exception as e:
            print(f"Error : {e}")
            messagebox.showerror(title ="Error in open project" , message=f"{e}")
            return

        self.root.after(0, self.wait.waiting)
        try:
            message = send_requiest(data["api_key"] , codes + self.promt_saver)
            self.promt_saver = ""
            self.root.after(0, self._add_message(message, sender="operator"))
        except Exception as e:
            print(f"Error : {e}")
            messagebox.showerror(title="Error" , message=f"{e}")
        self.root.after(0, self.wait.end_wait)

    def _add_message(self, text, sender="user"):
        # قاب حباب
        bubble_frame = tk.Frame(self.message_frame, bg="white")
        bubble_frame.pack(fill="x", pady=2)

        if sender == "user":
            lbl = tk.Label(
                bubble_frame, text=text, bg="#cce5ff", fg="black",
                wraplength=250, justify="right", anchor="e", padx=10, pady=5
            )
            lbl.pack(anchor="e", padx=10)
        else:
            lbl = tk.Label(
                bubble_frame, text=text, bg="#d4edda", fg="black",
                wraplength=250, justify="left", anchor="w", padx=10, pady=5
            )
            lbl.pack(anchor="w", padx=10)


# if __name__ == "__main__":
#     root = tk.Tk()
#     chat = ChatWindow(root)
#     root.mainloop()





# def long_task(loading_win):
#     # شبیه‌سازی یک کار طولانی
#     time.sleep(5)
#     # بستن پنجره‌ی لودینگ بعد از پایان کار
#     loading_win.destroy()

# def start_task():
#     # ساخت پنجره‌ی لودینگ
#     loading_win = tk.Toplevel(root)
#     loading_win.title("Please Wait")
#     loading_win.geometry("200x100")
#     tk.Label(loading_win, text="Loading... Please wait").pack(expand=True)

#     # اجرای کار طولانی در یک Thread جدا
#     threading.Thread(target=long_task, args=(loading_win,), daemon=True).start()

# root = tk.Tk()
# root.title("Main Window")
# root.geometry("300x200")

# tk.Button(root, text="Start Task", command=start_task).pack(pady=50)

# root.mainloop()

############################################################################################################

# import tkinter as tk

# class ChatWindow:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Chat Window")

#         # ساخت Canvas و Scrollbar
#         self.canvas = tk.Canvas(root, width=400, height=300)
#         self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
#         self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#         self.canvas.pack(fill=tk.BOTH, expand=True)

#         # اتصال اسکرول
#         self.canvas.configure(yscrollcommand=self.scrollbar.set)

#         # ساخت Frame داخل Canvas
#         self.message_frame = tk.Frame(self.canvas)
#         self.canvas.create_window((0, 0), window=self.message_frame, anchor="nw")

#         # تنظیم اسکرول هنگام تغییر اندازه
#         self.message_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

#         # فعال‌سازی اسکرول موس روی کل برنامه
#         self.root.bind_all("<MouseWheel>", self._on_mousewheel)   # ویندوز/مک
#         self.root.bind_all("<Button-4>", self._on_mousewheel)     # لینوکس بالا
#         self.root.bind_all("<Button-5>", self._on_mousewheel)     # لینوکس پایین

#         # ورودی و دکمه ارسال
#         self.entry = tk.Entry(root, width=40)
#         self.entry.pack(side=tk.LEFT, padx=5, pady=5)
#         self.send_button = tk.Button(root, text="ارسال", command=self.send_message)
#         self.send_button.pack(side=tk.LEFT, padx=5)

#     def _on_mousewheel(self, event):
#         """اسکرول موس روی canvas حتی وقتی موس روی message_frame یا ویجت‌های داخلشه"""
#         bbox = self.canvas.bbox("all")
#         if not bbox:
#             return

#         content_height = bbox[3] - bbox[1]
#         canvas_height = self.canvas.winfo_height()

#         if content_height <= canvas_height:
#             return

#         # ویندوز/مک
#         if event.delta:
#             self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
#         # لینوکس
#         elif event.num == 4:
#             self.canvas.yview_scroll(-1, "units")
#         elif event.num == 5:
#             self.canvas.yview_scroll(1, "units")

#     def send_message(self , alighn):
#         message = self.entry.get().strip()
#         if message:
#             self._add_message(f"کاربر: {message}", bg="lightblue" , alighn= alighn)
#             self.entry.delete(0, tk.END)

#     def receive_message(self, message , alighn):
#         self._add_message(f"اپراتور: {message}", bg="lightgreen" , alighn= alighn)

#     def _add_message(self, text, bg="white" , alighn = "left"):
#         box = tk.Text(self.message_frame, height=3, wrap="word", bg=bg )
#         box.tag_configure(alighn, justify=alighn)
#         box.insert(tk.END, text , alighn)
#         box.config(state="disabled")
#         box.pack(fill="x" , padx=5, pady=5)

# # اجرای برنامه
# if __name__ == "__main__":
#     root = tk.Tk()
#     chat = ChatWindow(root)
#     # اضافه کردن چند پیام برای تست اسکرول
#     for i in range(20):
#         chat.receive_message(f"پیام تست شماره {i+1}" , "right")
#     root.mainloop()