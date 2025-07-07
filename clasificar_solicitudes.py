import tkinter as tk
from tkinter import ttk, messagebox
from config import conectar_bd

def clasificar_solicitudes(root):
    ventana = tk.Toplevel(root)
    ventana.title("Clasificar Solicitudes")
    ventana.state("zoomed")  # Pantalla completa
    ventana.configure(bg="#F0F8FF")

    contenedor = tk.Frame(ventana, bg="#F0F8FF", padx=40, pady=40)
    contenedor.pack(fill="both", expand=True)

    ttk.Label(contenedor, text="Clasificación de Solicitudes", font=("Arial", 18, "bold"), background="#F0F8FF").pack(pady=10)

    columnas = ("ID", "Usuario", "Descripción", "Gravedad")
    tabla = ttk.Treeview(contenedor, columns=columnas, show="headings")
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=150)
    tabla.pack(pady=10, fill="both", expand=True)

    def cargar():
        for row in tabla.get_children():
            tabla.delete(row)
        conn = conectar_bd()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT id, usuario_nombre, descripcion, gravedad FROM solicitudes WHERE gravedad = 'sin clasificar'")
                for fila in cur.fetchall():
                    tabla.insert("", "end", values=fila)
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

    def clasificar(grado):
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona una solicitud.")
            return
        datos = tabla.item(seleccionado[0], "values")
        solicitud_id = datos[0]

        conn = conectar_bd()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("UPDATE solicitudes SET gravedad = %s WHERE id = %s", (grado, solicitud_id))
                conn.commit()
                messagebox.showinfo("Éxito", f"Solicitud #{solicitud_id} clasificada como {grado}.")
                cargar()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

    marco_botones = tk.Frame(contenedor, bg="#F0F8FF")
    marco_botones.pack(pady=10)

    ttk.Button(marco_botones, text="Alta", command=lambda: clasificar("Alta")).grid(row=0, column=0, padx=10)
    ttk.Button(marco_botones, text="Media", command=lambda: clasificar("Media")).grid(row=0, column=1, padx=10)
    ttk.Button(marco_botones, text="Baja", command=lambda: clasificar("Baja")).grid(row=0, column=2, padx=10)

    cargar()
