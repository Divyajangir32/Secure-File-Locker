import tkinter as tk
from tkinter import filedialog, messagebox
import os
from crypto_utils import encrypt_file, decrypt_file

root = tk.Tk()
root.title("Secure File Locker")
root.geometry("1100x650")
root.configure(bg="#0f172a")
root.iconbitmap("icon.ico")

# ---------------- PASSWORD ----------------
password_var = tk.StringVar()

def toggle_password():
    if password_entry.cget("show") == "":
        password_entry.config(show="•")
        show_btn.config(text="Show")
    else:
        password_entry.config(show="")
        show_btn.config(text="Hide")

# ---------------- SIDEBAR ----------------
sidebar = tk.Frame(root, bg="#020617", width=260)
sidebar.pack(side="left", fill="y")

tk.Label(
    sidebar,
    text="🔐 Secure\nFile Locker",
    font=("Segoe UI", 18, "bold"),
    fg="white",
    bg="#020617"
).pack(pady=30)

tk.Label(
    sidebar,
    text="Password",
    fg="#94a3b8",
    bg="#020617",
    font=("Segoe UI", 10)
).pack(anchor="w", padx=30)

password_entry = tk.Entry(
    sidebar,
    textvariable=password_var,
    show="•",
    font=("Segoe UI", 12),
    width=18
)
password_entry.pack(padx=30, pady=(5, 5))

show_btn = tk.Button(
    sidebar, text="Show",
    command=toggle_password,
    bg="#020617",
    fg="white",
    bd=0,
    cursor="hand2"
)
show_btn.pack(anchor="w", padx=30)

# ---------------- CONTENT ----------------
content = tk.Frame(root, bg="#0f172a")
content.pack(expand=True, fill="both")

title = tk.Label(
    content,
    text="Secure File Locker",
    font=("Segoe UI", 26, "bold"),
    bg="#0f172a",
    fg="white"
)
title.pack(pady=(60, 10))

subtitle = tk.Label(
    content,
    text="Encrypt files safely. Decrypt only with correct password.",
    font=("Segoe UI", 12),
    bg="#0f172a",
    fg="#94a3b8"
)
subtitle.pack()

file_label = tk.Label(
    content,
    text="No file selected",
    bg="#0f172a",
    fg="#e5e7eb",
    font=("Segoe UI", 11)
)
file_label.pack(pady=40)

# ---------------- BUTTON STYLE ----------------
def action_button(text, color, cmd):
    return tk.Button(
        sidebar,
        text=text,
        command=cmd,
        font=("Segoe UI", 11, "bold"),
        bg=color,
        fg="white",
        bd=0,
        padx=20,
        pady=10,
        cursor="hand2"
    )

# ---------------- ACTIONS ----------------
def encrypt_action():
    password = password_var.get().strip()

    if not password:
        messagebox.showerror("Error", "Enter password")
        return

    file_path = filedialog.askopenfilename(
        title="Select file to encrypt",
        initialdir=os.path.expanduser("~"),
        filetypes=[("All Files", "*.*")]
    )

    if not file_path:
        return

    try:
        encrypted_path = encrypt_file(file_path, password)
        messagebox.showinfo(
            "Success",
            f"File encrypted successfully!\nSaved in:\n{encrypted_path}"
        )
    except Exception as e:
        messagebox.showerror("Error", str(e))


def decrypt_action():
    password = password_var.get().strip()

    if not password:
        messagebox.showerror("Error", "Enter password")
        return

    file_path = filedialog.askopenfilename(
        title="Select encrypted file",
        initialdir="locker",
        filetypes=[("Encrypted Files", "*.lock")]
    )

    if not file_path:
        return

    try:
        output_path = decrypt_file(file_path, password)
        messagebox.showinfo(
            "Success",
            f"File decrypted successfully!\nRestored as:\n{output_path}"
        )
    except ValueError:
        messagebox.showerror("Error", "Wrong password")
    except Exception as e:
        messagebox.showerror("Error", str(e))



# ---------------- BUTTONS ----------------
action_button("🔒 Encrypt File", "#22c55e", encrypt_action).pack(pady=15)
action_button("🔓 Decrypt File", "#3b82f6", decrypt_action).pack(pady=10)
action_button("❌ Exit", "#ef4444", root.quit).pack(pady=40)

root.mainloop()
