# nuevo_admin.py
import tkinter as tk
from tkinter import ttk, messagebox
from config import conectar_bd

def nuevo_admin(root):
    win = tk.Toplevel(root)
    win.title("Registrar Administrador")
    win.geometry("300x350")

    ttk.Label(win, text="Nombre:").pack(pady=5)
    nombre = ttk.Entry(win)
    nombre.pack()

    ttk.Label(win, text="Contraseña:").pack(pady=5)
    contrasena = ttk.Entry(win, show="*")
    contrasena.pack()

    ttk.Label(win, text="Correo:").pack(pady=5)
    correo = ttk.Entry(win)
    correo.pack()

    ttk.Label(win, text="Teléfono:").pack(pady=5)
    telefono = ttk.Entry(win)
    telefono.pack()

    def registrar():
        nombre_val = nombre.get().strip()
        contra_val = contrasena.get().strip()
        correo_val = correo.get().strip()
        telefono_val = telefono.get().strip()

        if not nombre_val or not contra_val or not correo_val or not telefono_val:
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
            return

        conn = conectar_bd()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("INSERT INTO admin (nombre, contrasena, correo, telefono) VALUES (%s, %s, %s, %s)",
                            (nombre_val, contra_val, correo_val, telefono_val))
                conn.commit()
                messagebox.showinfo("Éxito", "Administrador registrado correctamente.")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar: {e}")
            finally:
                conn.close()

    ttk.Button(win, text="Registrar", command=registrar).pack(pady=15)
