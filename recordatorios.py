# recordatorios.py corregido sin botón de marcar como realizado
import tkinter as tk
from tkinter import ttk, messagebox
from config import conectar_bd
from tkcalendar import DateEntry
from datetime import datetime

def crear_recordatorio(root, usuario):
    win = tk.Toplevel(root)
    win.title("Mis Recordatorios")
    win.geometry("750x550")
    win.configure(bg="#E6F0FA")

    # --- FORMULARIO ---
    ttk.Label(win, text="Crear nuevo recordatorio", font=("Arial", 13, "bold")).pack(pady=5)
    frame_form = ttk.Frame(win)
    frame_form.pack(pady=10)

    titulo = tk.StringVar()
    mensaje = tk.StringVar()
    fecha = tk.StringVar()

    ttk.Label(frame_form, text="Título:").grid(row=0, column=0, padx=5, pady=5)
    ttk.Entry(frame_form, textvariable=titulo, width=30).grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_form, text="Mensaje:").grid(row=1, column=0, padx=5, pady=5)
    ttk.Entry(frame_form, textvariable=mensaje, width=30).grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame_form, text="Fecha:").grid(row=2, column=0, padx=5, pady=5)
    fecha_entry = DateEntry(frame_form, textvariable=fecha, width=28, background='darkblue',
                            foreground='white', date_pattern='yyyy-mm-dd')
    fecha_entry.grid(row=2, column=1, padx=5, pady=5)

    def guardar():
        t = titulo.get().strip()
        m = mensaje.get().strip()
        f = fecha.get().strip()

        if not t or not m or not f:
            messagebox.showwarning("Campos Vacíos", "Todos los campos son obligatorios.")
            return

        conn = conectar_bd()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("INSERT INTO recordatorios (usuario_nombre, titulo, mensaje, fecha, estado) VALUES (%s, %s, %s, %s, %s)",
                            (usuario, t, m, f, "pendiente"))
                conn.commit()
                messagebox.showinfo("Guardado", "Recordatorio creado correctamente.")
                titulo.set("")
                mensaje.set("")
                fecha_entry.set_date(datetime.today())
                cargar_tabla()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

    ttk.Button(frame_form, text="Guardar Recordatorio", command=guardar).grid(columnspan=2, pady=10)

    # --- TABLA ---
    ttk.Label(win, text="Recordatorios Registrados", font=("Arial", 13, "bold")).pack()
    frame_tabla = ttk.Frame(win)
    frame_tabla.pack(fill="both", expand=True, padx=10)

    tabla = ttk.Treeview(frame_tabla, columns=("ID", "Título", "Mensaje", "Fecha", "Estado"), show="headings")
    for col in ("ID", "Título", "Mensaje", "Fecha", "Estado"):
        tabla.heading(col, text=col)
        tabla.column(col, width=120)
    tabla.pack(fill="both", expand=True)

    def cargar_tabla():
        for i in tabla.get_children():
            tabla.delete(i)
        conn = conectar_bd()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT id, titulo, mensaje, fecha, estado FROM recordatorios WHERE usuario_nombre = %s", (usuario,))
                for fila in cur.fetchall():
                    tabla.insert("", "end", values=fila)
            except Exception as e:
                messagebox.showerror("Error al cargar", str(e))
            finally:
                conn.close()

    def eliminar():
        item = tabla.selection()
        if not item:
            messagebox.showwarning("Selecciona", "Selecciona un recordatorio para eliminar.")
            return
        datos = tabla.item(item[0])["values"]
        rid = datos[0]
        confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar el recordatorio #{rid}?")
        if confirmar:
            conn = conectar_bd()
            if conn:
                try:
                    cur = conn.cursor()
                    cur.execute("DELETE FROM recordatorios WHERE id = %s AND usuario_nombre = %s", (rid, usuario))
                    conn.commit()
                    cargar_tabla()
                    messagebox.showinfo("Eliminado", "Recordatorio eliminado.")
                except Exception as e:
                    messagebox.showerror("Error al eliminar", str(e))
                finally:
                    conn.close()

    def editar():
        item = tabla.selection()
        if not item:
            messagebox.showwarning("Selecciona", "Selecciona un recordatorio para editar.")
            return
        datos = tabla.item(item[0])["values"]
        rid = datos[0]
        titulo.set(datos[1])
        mensaje.set(datos[2])
        fecha_entry.set_date(datos[3])

        def actualizar():
            conn = conectar_bd()
            if conn:
                try:
                    cur = conn.cursor()
                    cur.execute("UPDATE recordatorios SET titulo=%s, mensaje=%s, fecha=%s WHERE id = %s AND usuario_nombre = %s",
                                (titulo.get(), mensaje.get(), fecha.get(), rid, usuario))
                    conn.commit()
                    messagebox.showinfo("Actualizado", "Recordatorio actualizado.")
                    titulo.set("")
                    mensaje.set("")
                    fecha_entry.set_date(datetime.today())
                    cargar_tabla()
                except Exception as e:
                    messagebox.showerror("Error al actualizar", str(e))
                finally:
                    conn.close()

        ttk.Button(frame_form, text="Guardar Cambios", command=actualizar).grid(columnspan=2, pady=5)

    # --- BOTONES DE ACCIÓN ---
    frame_botones = ttk.Frame(win)
    frame_botones.pack(pady=10)

    ttk.Button(frame_botones, text="Editar Seleccionado", command=editar).grid(row=0, column=0, padx=5)
    ttk.Button(frame_botones, text="Eliminar Seleccionado", command=eliminar).grid(row=0, column=1, padx=5)
    ttk.Button(frame_botones, text="Cerrar", command=win.destroy).grid(row=0, column=2, padx=5)

    cargar_tabla()
