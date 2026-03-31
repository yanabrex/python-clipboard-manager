import pyperclip
import time
import json
import os
import threading
import tkinter as tk
from tkinter import messagebox

last_clip = ""
history = []
# check if the json file exists or is empty, otherwise create it or formate it properly with []
if not os.path.exists("clipboard.json") or os.path.getsize("clipboard.json") == 0:
    with open("clipboard.json", "w") as f:
        json.dump([], f)

try:
    with open("clipboard.json", "r") as f:
        history = json.load(f)
except FileNotFoundError:
    history = []
# create a GUI window with a title Clipboard Manager
root = tk.Tk()
root.title("Clipboard Manager")

listbox = tk.Listbox(root, width=50, height=15)
listbox.pack(padx=10, pady=10)

def update_listbox():
    listbox.delete(0, tk.END)
    for item in history[-50:]: # only last 50 items in history to prevent it from growing too big
        listbox.insert(tk.END, item)

def clear_history():
    global history
    history = []
    update_listbox()
    with open("clipboard.json", "w") as f:
        json.dump(history, f, indent=2)
    messagebox.showinfo("Clipboard Manager", "History Cleared!")

def copy_selected():
    try:
        selection = listbox.get(listbox.curselection())
        pyperclip.copy(selection)
        messagebox.showinfo("Clipboard Manager", f"Copied: {selection}")
    except tk.TclError:
        messagebox.showwarning("Clipboard Manager", "No item selected")

tk.Button(root, text="Clear History", command = clear_history).pack(pady=5)
tk.Button(root, text="Copy Selected", command = copy_selected).pack(pady=5)

update_listbox()

def scan_clipboard():
    last_clip = ""
    while True:
        current = pyperclip.paste().strip()
        if current != last_clip and current != "":
            history.append(current)
            history[-50:] # only last 50 items
            with open("clipboard.json", "w") as f:
                json.dump(history[-50:], f, indent=2)
            last_clip = current

            root.after(0, update_listbox)
        # scan in a one second interval
        time.sleep(1)

threading.Thread(target = scan_clipboard, daemon = True).start()

root.mainloop()
