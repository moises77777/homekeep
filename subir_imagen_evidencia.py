import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from config import conectar_bd
import shutil
import os

def subir_imagen_evidencia(root, usuario):
    ventana = tk.Toplevel(root)
    ventana.title("Subir Imagen de Evidencia")
    ventana.state("zoomed")  # Pantalla completa
    ventana.configure(bg="#F0F8FF")

    contenedor = tk.Frame(ventana, bg="#F0F8FF", padx=40, pady=40)
    contenedor.pack(expand=True, fill="both")

    ttk.Label(contenedor, text="Subir Imagen a una Solicitud", font=("Arial", 18, "bold"), background="#F0F8FF").pack(pady=10)

    ttk.Label(contenedor, text="ID de la solicitud:", background="#F0F8FF").pack(anchor="w", pady=5)
    solicitud_id = tk.StringVar()
    ttk.Entry(contenedor, textvariable=solicitud_id, width=30).pack(pady=5)

    ttk.Label(contenedor, text="Seleccionar imagen:", background="#F0F8FF").pack(anchor="w", pady=10)

    ruta_imagen = tk.StringVar()

    def seleccionar_imagen():
        archivo = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg")])
        if archivo:
            ruta_imagen.set(archivo)
            lbl_ruta.config(text=os.path.basename(archivo))

    ttk.Button(contenedor, text="Seleccionar Archivo", command=seleccionar_imagen).pack(pady=5)
    lbl_ruta = ttk.Label(contenedor, text="", background="#F0F8FF")
    lbl_ruta.pack()

    def guardar_imagen():
        sid = solicitud_id.get().strip()
        ruta = ruta_imagen.get().strip()

        if not sid or not ruta:
            messagebox.showwarning("Atención", "Completa todos los campos y selecciona una imagen.")
            return

        # Crear carpeta si no existe
        if not os.path.exists("imagenes"):
            os.makedirs("imagenes")

        nombre_archivo = os.path.basename(ruta)
        destino = os.path.join("imagenes", nombre_archivo)

        try:
            shutil.copy(ruta, destino)
        except Exception as e:
            messagebox.showerror("Error al copiar imagen", str(e))
            return

        conn = conectar_bd()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("UPDATE solicitudes SET imagen_path = %s WHERE id = %s AND usuario_nombre = %s", (destino, sid, usuario))
                conn.commit()
                messagebox.showinfo("Éxito", "Imagen subida correctamente.")
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

    ttk.Button(contenedor, text="Subir Imagen", command=guardar_imagen).pack(pady=20)
