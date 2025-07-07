import tkinter as tk
from tkinter import ttk, messagebox
from config import conectar_bd

def ver_estado_solicitudes(root, usuario):
    ventana = tk.Toplevel(root)
    ventana.title("Estado de Solicitudes")
    ventana.state("zoomed")  # Pantalla completa
    ventana.configure(bg="#F0F8FF")

    contenedor = tk.Frame(ventana, bg="#F0F8FF", padx=40, pady=40)
    contenedor.pack(expand=True, fill="both")

    ttk.Label(contenedor, text=f"Solicitudes de {usuario}", font=("Arial", 18, "bold"), background="#F0F8FF").pack(pady=10)

    columnas = ("ID", "Descripción", "Estado", "Gravedad")
    tabla = ttk.Treeview(contenedor, columns=columnas, show="headings")
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=150)
    tabla.pack(pady=10, fill="both", expand=True)

    def cargar_solicitudes():
        for row in tabla.get_children():
            tabla.delete(row)

        conn = conectar_bd()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT id, descripcion, estado, gravedad FROM solicitudes WHERE usuario_nombre = %s", (usuario,))
                for fila in cur.fetchall():
                    tabla.insert("", "end", values=fila)
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

    def eliminar_solicitud():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una solicitud para eliminar.")
            return

        datos = tabla.item(seleccion[0], "values")
        id_solicitud = datos[0]

        confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar solicitud #{id_solicitud}?")
        if confirmar:
            conn = conectar_bd()
            if conn:
                try:
                    cur = conn.cursor()
                    cur.execute("DELETE FROM solicitudes WHERE id = %s AND usuario_nombre = %s", (id_solicitud, usuario))
                    conn.commit()
                    messagebox.showinfo("Éxito", "Solicitud eliminada.")
                    cargar_solicitudes()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                finally:
                    conn.close()

    ttk.Button(contenedor, text="Eliminar Solicitud Seleccionada", command=eliminar_solicitud).pack(pady=10)

    cargar_solicitudes()
