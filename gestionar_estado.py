import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from config import conectar_bd
import os

def gestionar_estado_solicitud(root):
    ventana = tk.Toplevel(root)
    ventana.title("Gestionar Estado de Solicitudes")
    ventana.geometry("900x500")
    ventana.configure(bg="#F0F8FF")

    tabla = ttk.Treeview(ventana, columns=("id", "usuario", "descripcion", "estado", "gravedad"), show="headings")
    tabla.heading("id", text="ID")
    tabla.heading("usuario", text="Usuario")
    tabla.heading("descripcion", text="Descripción")
    tabla.heading("estado", text="Estado")
    tabla.heading("gravedad", text="Gravedad")
    tabla.column("descripcion", width=300)
    tabla.pack(fill="both", expand=True, pady=10)

    def cargar():
        for i in tabla.get_children():
            tabla.delete(i)
        conn = conectar_bd()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, usuario_nombre, descripcion, estado, gravedad FROM solicitudes")
                for row in cursor.fetchall():
                    tabla.insert("", "end", values=row)
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

    def ver_imagen():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona una solicitud.")
            return

        solicitud_id = tabla.item(seleccionado)["values"][0]

        conn = conectar_bd()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT imagen_path FROM solicitudes WHERE id = %s", (solicitud_id,))
                resultado = cursor.fetchone()
                if resultado and resultado[0] and os.path.exists(resultado[0]):
                    imagen_ventana = tk.Toplevel(ventana)
                    imagen_ventana.title("Imagen Evidencia")

                    img = Image.open(resultado[0])
                    img = img.resize((400, 400))
                    img_tk = ImageTk.PhotoImage(img)

                    label = tk.Label(imagen_ventana, image=img_tk)
                    label.image = img_tk
                    label.pack()
                else:
                    messagebox.showinfo("Sin imagen", "No hay imagen para esta solicitud.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

    def actualizar_estado_gravedad():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona una solicitud.")
            return

        solicitud_id = tabla.item(seleccionado)["values"][0]
        nuevo_estado = combo_estado.get()
        nueva_gravedad = combo_gravedad.get()

        if not nuevo_estado or not nueva_gravedad:
            messagebox.showwarning("Advertencia", "Selecciona un estado y una gravedad.")
            return

        conn = conectar_bd()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE solicitudes SET estado = %s, gravedad = %s WHERE id = %s",
                               (nuevo_estado, nueva_gravedad, solicitud_id))
                conn.commit()
                messagebox.showinfo("Éxito", "Solicitud actualizada.")
                cargar()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

    def eliminar_solicitud():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona una solicitud.")
            return

        solicitud_id = tabla.item(seleccionado)["values"][0]

        respuesta = messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar esta solicitud?")
        if respuesta:
            conn = conectar_bd()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM solicitudes WHERE id = %s", (solicitud_id,))
                    conn.commit()
                    messagebox.showinfo("Éxito", "Solicitud eliminada.")
                    cargar()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                finally:
                    conn.close()

    opciones_frame = ttk.Frame(ventana, padding=10)
    opciones_frame.pack()

    ttk.Label(opciones_frame, text="Nuevo Estado:").grid(row=0, column=0, padx=5, pady=5)
    combo_estado = ttk.Combobox(opciones_frame, values=["pendiente", "en proceso", "resuelto"])
    combo_estado.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(opciones_frame, text="Gravedad:").grid(row=0, column=2, padx=5, pady=5)
    combo_gravedad = ttk.Combobox(opciones_frame, values=["baja", "media", "alta"])
    combo_gravedad.grid(row=0, column=3, padx=5, pady=5)

    ttk.Button(opciones_frame, text="Actualizar", command=actualizar_estado_gravedad).grid(row=0, column=4, padx=5, pady=5)
    ttk.Button(opciones_frame, text="Ver Imagen", command=ver_imagen).grid(row=0, column=5, padx=5, pady=5)
    ttk.Button(opciones_frame, text="Eliminar", command=eliminar_solicitud).grid(row=0, column=6, padx=5, pady=5)
    ttk.Button(opciones_frame, text="Volver", command=ventana.destroy).grid(row=0, column=7, padx=5, pady=5)

    cargar()
