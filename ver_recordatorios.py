import tkinter as tk
from tkinter import ttk, messagebox
from config import conectar_bd

def ver_recordatorios(root, usuario):
    win = tk.Toplevel(root)
    win.title("Mis Recordatorios")
    win.configure(bg="#E6F0FA")
    win.geometry("900x500")

    try:
        logo = tk.PhotoImage(file="logo.png")
        tk.Label(win, image=logo, bg="#E6F0FA").pack(pady=5)
        win.logo = logo
    except:
        pass

    tk.Label(win, text=f"Recordatorios de {usuario}", font=("Arial", 16, "bold"), bg="#E6F0FA").pack(pady=10)

    tabla_frame = tk.Frame(win, bg="#E6F0FA")
    tabla_frame.pack(pady=10, fill="both", expand=True)

    tabla = ttk.Treeview(tabla_frame, columns=("ID", "Título", "Mensaje", "Fecha"), show="headings")
    tabla.heading("ID", text="ID")
    tabla.heading("Título", text="Título")
    tabla.heading("Mensaje", text="Mensaje")
    tabla.heading("Fecha", text="Fecha")
    tabla.column("ID", width=50)
    tabla.column("Título", width=200)
    tabla.column("Mensaje", width=400)
    tabla.column("Fecha", width=100)
    tabla.pack(fill="both", expand=True)

    try:
        conn = conectar_bd()
        cur = conn.cursor()
        cur.execute("SELECT id, titulo, mensaje, fecha FROM recordatorios WHERE usuario_nombre = %s", (usuario,))
        resultados = cur.fetchall()

        for fila in resultados:
            tabla.insert("", "end", values=fila)

        cur.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los recordatorios: {str(e)}")

    tk.Button(win, text="Volver", command=win.destroy).pack(pady=10)
