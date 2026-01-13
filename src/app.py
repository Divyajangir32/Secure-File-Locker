import tkinter as tk
from tkinter import filedialog, messagebox
from crypto_utils import encrypt_file, decrypt_file
import os, re

attempts = 0
MAX_ATTEMPTS = 3

root = tk.Tk()
root.title("Secure File Locker")
root.geometry("420x360")
root.resizable(False, False)
root.config(bg="#0F172A")

# Title
tk.Label(root, text="🔐 Secure File Locker",
         font=("Segoe UI",18,"bold"),
         fg="white", bg="#0F172A").pack(pady=16)

tk.Label(root, text="Enter Your Secret Password",
         fg="white", bg="#0F172A",
         font=("Segoe UI",11)).pack()

password_entry = tk.Entry(root, show="*", width=28, font=("Segoe UI",12))
password_entry.pack(pady=8)

# ---------- SHOW / HIDE PASSWORD ----------
show_pwd = False
def toggle_password():
    global show_pwd
    if show_pwd:
        password_entry.config(show="*")
        eye_btn.config(text="👁 Show")
        show_pwd = False
    else:
        password_entry.config(show="")
        eye_btn.config(text="🙈 Hide")
        show_pwd = True

eye_btn = tk.Button(root, text="👁 Show", bg="#0F172A", fg="white",
                    relief="flat", font=("Segoe UI",10,"bold"),
                    command=toggle_password)
eye_btn.pack(pady=4)
# ------------------------------------------

def shake_window():
    x = root.winfo_x()
    y = root.winfo_y()
    for i in range(10):
        root.geometry(f"+{x+10}+{y}")
        root.update()
        root.after(25)
        root.geometry(f"+{x-10}+{y}")
        root.update()
        root.after(25)
    root.geometry(f"+{x}+{y}")

def is_strong_password(pwd):
    if len(pwd) < 8: return False
    if not re.search(r"[A-Z]", pwd): return False
    if not re.search(r"[a-z]", pwd): return False
    if not re.search(r"[0-9]", pwd): return False
    if not re.search(r"[@$!%*?&]", pwd): return False
    return True

def upload_file():
    global attempts
    file_path = filedialog.askopenfilename()
    if not file_path: return

    pwd = password_entry.get()
    if pwd == "":
        messagebox.showerror("Error", "Please enter password")
        return

    if not is_strong_password(pwd):
        attempts += 1
        remaining = MAX_ATTEMPTS - attempts
        shake_window()
        if attempts >= MAX_ATTEMPTS:
            messagebox.showerror("LOCKED","Too many failed attempts!\nApplication locked.")
            root.destroy()
        else:
            messagebox.showerror("Weak Password", f"Weak password!\nAttempts left: {remaining}")
        return

    encrypt_file(file_path, pwd)
    messagebox.showinfo("Success","File Encrypted & Stored Successfully!")

def download_file():
    file_path = filedialog.askopenfilename(initialdir="../locker/")
    if file_path:
        decrypt_file(os.path.basename(file_path), password_entry.get())
        messagebox.showinfo("Done","File Decrypted Successfully!")

def view_files():
    if not os.path.exists("../locker"):
        os.mkdir("../locker")
    files = os.listdir("../locker")
    if not files:
        messagebox.showinfo("Locker","No encrypted files found.")
    else:
        messagebox.showinfo("Encrypted Files","\n".join(files))

def delete_file():
    file_path = filedialog.askopenfilename(initialdir="../locker")
    if file_path:
        os.remove(file_path)
        messagebox.showinfo("Deleted","Encrypted file deleted successfully!")

# ---------- Buttons ----------
tk.Button(root, text="Encrypt & Store", bg="#22C55E",
          fg="black", width=22, font=("Segoe UI",11,"bold"),
          command=upload_file).pack(pady=8)

tk.Button(root, text="Decrypt & Download", bg="#38BDF8",
          fg="black", width=22, font=("Segoe UI",11,"bold"),
          command=download_file).pack(pady=4)

tk.Button(root, text="View Encrypted Files", bg="#3498DB",
          fg="white", width=22, command=view_files).pack(pady=4)

tk.Button(root, text="Delete Encrypted File", bg="#E74C3C",
          fg="white", width=22, command=delete_file).pack(pady=4)

tk.Label(root, text="Developed by Divya Jangir | Secure File Locker v2.0",
         bg="#0F172A", fg="#94A3B8", font=("Segoe UI",9)).pack(side="bottom", pady=6)

root.mainloop()
