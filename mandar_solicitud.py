import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from config import conectar_bd
import shutil
import os

def mandar_solicitud(root, usuario):
    win = tk.Toplevel(root)
    win.title("Mandar Solicitud")
    win.geometry("800x600")
    win.configure(bg="#F0F8FF")

    # FORMULARIO
    ttk.Label(win, text="Crear nueva solicitud", font=("Arial", 13, "bold")).pack(pady=5)
    frame_form = ttk.Frame(win)
    frame_form.pack(pady=5)

    titulo = tk.StringVar()
    gravedad = tk.StringVar()
    imagen_path = tk.StringVar()

    ttk.Label(frame_form, text="Título:").grid(row=0, column=0, padx=5, pady=5)
    entry_titulo = ttk.Entry(frame_form, textvariable=titulo, width=40)
    entry_titulo.grid(row=0, column=1, padx=5)

    ttk.Label(frame_form, text="Descripción:").grid(row=1, column=0, padx=5, pady=5)
    descripcion_txt = tk.Text(frame_form, height=4, width=30)
    descripcion_txt.grid(row=1, column=1, padx=5)

    ttk.Label(frame_form, text="Gravedad (alta, media, baja):").grid(row=2, column=0, padx=5, pady=5)
    entry_gravedad = ttk.Entry(frame_form, textvariable=gravedad)
    entry_gravedad.grid(row=2, column=1, padx=5)

    ttk.Label(frame_form, text="Imagen (opcional):").grid(row=3, column=0, padx=5, pady=5)
    entry_imagen = ttk.Entry(frame_form, textvariable=imagen_path, width=30)
    entry_imagen.grid(row=3, column=1, padx=5)
    ttk.Button(frame_form, text="Seleccionar Imagen", command=lambda: seleccionar_imagen(imagen_path)).grid(row=3, column=2)

    def guardar():
        t = titulo.get().strip()
        d = descripcion_txt.get("1.0", "end").strip()
        g = gravedad.get().strip().lower()
        i = imagen_path.get().strip()
        ruta_destino = ""

        if not t or not d or not g:
            messagebox.showwarning("Campos Vacíos", "Completa todos los campos obligatorios.")
            return

        if i:
            try:
                os.makedirs("evidencias", exist_ok=True)
                nombre_archivo = os.path.basename(i)
                ruta_destino = os.path.join("evidencias", nombre_archivo)
                shutil.copy(i, ruta_destino)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo copiar la imagen: {e}")
                return

        conn = conectar_bd()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("INSERT INTO solicitudes (usuario_nombre, titulo, descripcion, gravedad, imagen, estado) VALUES (%s, %s, %s, %s, %s, %s)",
                            (usuario, t, d, g, ruta_destino, "pendiente"))
                conn.commit()
                messagebox.showinfo("Éxito", "Solicitud enviada.")
                titulo.set("")
                gravedad.set("")
                imagen_path.set("")
                descripcion_txt.delete("1.0", "end")
                cargar_tabla()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

    ttk.Button(frame_form, text="Enviar Solicitud", command=guardar).grid(columnspan=3, pady=10)

    # TABLA PARA VER Y EDITAR
    ttk.Label(win, text="Mis Solicitudes Registradas", font=("Arial", 13, "bold")).pack(pady=5)
    frame_tabla = ttk.Frame(win)
    frame_tabla.pack(fill="both", expand=True, padx=10)

    tabla = ttk.Treeview(frame_tabla, columns=("ID", "Título", "Descripción", "Gravedad", "Estado"), show="headings")
    for col in tabla["columns"]:
        tabla.heading(col, text=col)
        tabla.column(col, width=130)
    tabla.pack(fill="both", expand=True)

    def cargar_tabla():
        for i in tabla.get_children():
            tabla.delete(i)
        conn = conectar_bd()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT id, titulo, descripcion, gravedad, estado FROM solicitudes WHERE usuario_nombre = %s", (usuario,))
                for fila in cur.fetchall():
                    tabla.insert("", "end", values=fila)
            except Exception as e:
                messagebox.showerror("Error al cargar solicitudes", str(e))
            finally:
                conn.close()

    def seleccionar_imagen(var):
        ruta = filedialog.askopenfilename(title="Seleccionar Imagen", filetypes=[("Archivos de imagen", "*.jpg *.png *.jpeg")])
        if ruta:
            var.set(ruta)

    def editar_solicitud():
        item = tabla.selection()
        if not item:
            messagebox.showwarning("Selecciona", "Selecciona una solicitud para editar.")
            return

        datos = tabla.item(item[0])["values"]
        sid = datos[0]

        titulo.set(datos[1])
        descripcion_txt.delete("1.0", "end")
        descripcion_txt.insert("1.0", datos[2])
        gravedad.set(datos[3])

        def actualizar():
            t = titulo.get().strip()
            d = descripcion_txt.get("1.0", "end").strip()
            g = gravedad.get().strip().lower()

            if not t or not d or not g:
                messagebox.showwarning("Campos Vacíos", "Completa todos los campos.")
                return

            conn = conectar_bd()
            if conn:
                try:
                    cur = conn.cursor()
                    cur.execute("UPDATE solicitudes SET titulo = %s, descripcion = %s, gravedad = %s WHERE id = %s AND usuario_nombre = %s",
                                (t, d, g, sid, usuario))
                    if cur.rowcount > 0:
                        conn.commit()
                        messagebox.showinfo("Éxito", "Solicitud actualizada.")
                        titulo.set("")
                        gravedad.set("")
                        imagen_path.set("")
                        descripcion_txt.delete("1.0", "end")
                        cargar_tabla()
                    else:
                        messagebox.showerror("Error", "No se pudo actualizar la solicitud.")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                finally:
                    conn.close()

        ttk.Button(frame_form, text="Guardar Cambios", command=actualizar).grid(columnspan=3, pady=5)

    ttk.Button(win, text="Editar Solicitud Seleccionada", command=editar_solicitud).pack(pady=5)
    ttk.Button(win, text="Cerrar", command=win.destroy).pack(pady=10)

    cargar_tabla()
