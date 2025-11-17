import tkinter as tk
from tkinter import ttk

def on_item_click(event):
    tree = event.widget
    selected_item = tree.focus()  # آیتم انتخاب‌شده
    path = []

    # حرکت از آیتم انتخاب‌شده تا ریشه
    while selected_item:
        path.insert(0, tree.item(selected_item, "text"))  # نام آیتم
        selected_item = tree.parent(selected_item)        # والد آیتم

    print("مسیر کامل:", " / ".join(path))

root = tk.Tk()
tree = ttk.Treeview(root)

# ساختار نمونه
root_node = tree.insert("", "end", text="Root")
child1 = tree.insert(root_node, "end", text="Child1")
child2 = tree.insert(root_node, "end", text="Child2")
subchild1 = tree.insert(child1, "end", text="SubChild1")
subchild2 = tree.insert(child1, "end", text="SubChild2")

tree.pack()

# اتصال رویداد کلیک
tree.bind("<ButtonRelease-1>", on_item_click)

root.mainloop()
