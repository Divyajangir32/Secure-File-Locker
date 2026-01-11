import tkinter as tk
from tkinter import filedialog, messagebox
from crypto_utils import encrypt_file, decrypt_file
import os

root = tk.Tk()
root.title("Secure File Locker")
root.geometry("420x300")
root.config(bg="#0F172A")   # Dark blue background

title = tk.Label(root, text="🔐 Secure File Locker", font=("Segoe UI",18,"bold"), fg="white", bg="#0F172A")
title.pack(pady=20)

tk.Label(root, text="Enter Your Secret Password", fg="white", bg="#0F172A", font=("Segoe UI",11)).pack()

password_entry = tk.Entry(root, show="*", width=28, font=("Segoe UI",12))
password_entry.pack(pady=8)

def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        encrypt_file(file_path, password_entry.get())
        messagebox.showinfo("Success", "File Encrypted & Stored Successfully!")

def download_file():
    file_path = filedialog.askopenfilename(initialdir="../locker/")
    if file_path:
        decrypt_file(os.path.basename(file_path), password_entry.get())
        messagebox.showinfo("Done", "File Decrypted Successfully!")

tk.Button(root, text="Encrypt & Store", bg="#22C55E", fg="black", width=22, font=("Segoe UI",11,"bold"), command=upload_file).pack(pady=10)
tk.Button(root, text="Decrypt & Download", bg="#38BDF8", fg="black", width=22, font=("Segoe UI",11,"bold"), command=download_file).pack()

root.mainloop()
