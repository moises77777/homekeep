import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
from config import conectar_bd
from nuevo_usuario import nuevo_usuario
from nuevo_admin import nuevo_admin
from agregar_vivienda import agregar_vivienda
from mandar_solicitud import mandar_solicitud
from recordatorios import crear_recordatorio
from ver_estado_solicitudes import ver_estado_solicitudes
from encuesta_satisfaccion import encuesta_satisfaccion
from ver_resultados_encuestas import ver_resultados_encuestas
from ver_comentarios import ver_comentarios_encuestas
from ver_usuarios import ver_usuarios
from ver_estadisticas import ver_estadisticas
from gestionar_estado import gestionar_estado_solicitud
from subir_imagen_evidencia import subir_imagen_evidencia
from admin_encuestas import admin_encuestas  # ✅ NUEVO
from flask import Flask, jsonify
from threading import Thread

# Crear la aplicación Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Bienvenido a mi página web"

# Ruta para mostrar información (ejemplo)
@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        'nombre': 'Mi Página Web',
        'descripción': 'Una página web accesible públicamente.'
    })

# Función de inicio de la aplicación Tkinter
def pantalla_inicio(root):
    for w in root.winfo_children():
        w.destroy()

    try:
        img = Image.open("logotipo.jpg")
        img = img.resize((120, 120))
        logo = ImageTk.PhotoImage(img)
        logo_label = tk.Label(root, image=logo, bg="#E6F0FA")
        logo_label.image = logo
        logo_label.pack(pady=10)
    except:
        pass

    tk.Label(root, text="Bienvenido a HomeKeep", font=("Arial", 18, "bold"), bg="#E6F0FA").pack(pady=10)
    ttk.Button(root, text="Continuar", command=lambda: mostrar_menu(root)).pack(pady=15)

def login(root, tipo):
    login_win = tk.Toplevel(root)
    login_win.title(f"Iniciar sesión como {tipo}")
    login_win.geometry("300x220")

    ttk.Label(login_win, text="Nombre:", font=("Arial", 12)).pack(pady=5)
    nombre = ttk.Entry(login_win)
    nombre.pack()

    ttk.Label(login_win, text="Contraseña:", font=("Arial", 12)).pack(pady=5)
    contra = ttk.Entry(login_win, show="*")
    contra.pack()

    def validar():
        nombre_val = nombre.get().strip()
        contra_val = contra.get().strip()
        conn = conectar_bd()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(f"SELECT * FROM {tipo} WHERE nombre = %s AND contrasena = %s", (nombre_val, contra_val))
                if cur.fetchone():
                    login_win.destroy()
                    menu_usuario(root, nombre_val, tipo)
                else:
                    messagebox.showerror("Error", "Credenciales inválidas.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

    ttk.Button(login_win, text="Ingresar", command=validar).pack(pady=15)

def menu_usuario(root, usuario, tipo):
    for w in root.winfo_children():
        w.destroy()

    try:
        img = Image.open("logotipo.jpg")
        img = img.resize((100, 100))
        logo = ImageTk.PhotoImage(img)
        logo_label = tk.Label(root, image=logo, bg="#E6F0FA")
        logo_label.image = logo
        logo_label.pack(pady=10)
    except:
        pass

    ttk.Label(root, text=f"Menú de {usuario}", font=("Arial", 16, "bold")).pack(pady=5)

    contenedor = ttk.Frame(root, padding=15)
    contenedor.pack(fill="both", expand=True)

    if tipo == "usuarios":
        box1 = ttk.LabelFrame(contenedor, text="Gestión de Solicitudes", padding=10)
        box1.pack(fill="x", expand=True, pady=10)
        ttk.Button(box1, text="Vivienda", command=lambda: agregar_vivienda(root, usuario)).pack(fill="x", pady=2)
        ttk.Button(box1, text="Mandar Solicitud", command=lambda: mandar_solicitud(root, usuario)).pack(fill="x", pady=2)
        ttk.Button(box1, text="Ver Estado de Solicitudes", command=lambda: ver_estado_solicitudes(root, usuario)).pack(fill="x", pady=2)

        box2 = ttk.LabelFrame(contenedor, text="Recordatorios", padding=10)
        box2.pack(fill="x", expand=True, pady=10)
        ttk.Button(box2, text="Crear Recordatorio", command=lambda: crear_recordatorio(root, usuario)).pack(fill="x", pady=2)

        box3 = ttk.LabelFrame(contenedor, text="Encuestas", padding=10)
        box3.pack(fill="x", expand=True, pady=10)
        ttk.Button(box3, text="Responder Encuesta de Satisfacción", command=lambda: encuesta_satisfaccion(root, usuario)).pack(fill="x", pady=2)
        ttk.Button(box3, text="Ver Resultados Globales", command=lambda: ver_resultados_encuestas(root)).pack(fill="x", pady=2)

        box4 = ttk.LabelFrame(contenedor, text="Evidencia", padding=10)
        box4.pack(fill="x", expand=True, pady=10)
        ttk.Button(box4, text="Subir Imagen Evidencia", command=lambda: subir_imagen_evidencia(root, usuario)).pack(fill="x", pady=2)

    elif tipo == "admin":
        box_admin = ttk.LabelFrame(contenedor, text="Panel de Administrador", padding=10)
        box_admin.pack(fill="x", expand=True, pady=10)
        ttk.Button(box_admin, text="Ver Usuarios Registrados", command=lambda: ver_usuarios(root)).pack(fill="x", pady=2)
        ttk.Button(box_admin, text="Ver Resultados de Encuestas", command=lambda: ver_resultados_encuestas(root)).pack(fill="x", pady=2)
        ttk.Button(box_admin, text="Ver Comentarios de Encuestas", command=lambda: ver_comentarios_encuestas(root)).pack(fill="x", pady=2)
        ttk.Button(box_admin, text="Ver Estadísticas del Sistema", command=lambda: ver_estadisticas(root)).pack(fill="x", pady=2)
        ttk.Button(box_admin, text="Gestionar Solicitudes", command=lambda: gestionar_estado_solicitud(root)).pack(fill="x", pady=2)
        ttk.Button(box_admin, text="Gestionar Encuestas (Preguntas y Comentarios)", command=lambda: admin_encuestas(root)).pack(fill="x", pady=2)

    ttk.Button(root, text="Cerrar Sesión", command=lambda: pantalla_inicio(root)).pack(pady=15)

def mostrar_menu(root):
    for w in root.winfo_children():
        w.destroy()

    try:
        img = Image.open("logotipo.jpg")
        img = img.resize((100, 100))
        logo = ImageTk.PhotoImage(img)
        logo_label = tk.Label(root, image=logo, bg="#000068")
        logo_label.image = logo
        logo_label.pack(pady=10)
    except:
        pass

    ttk.Label(root, text="HomeKeep - Sistema de Mantenimiento", font=("Arial", 16, "bold")).pack(pady=10)

    frame = ttk.Frame(root, padding=20)
    frame.pack()

    ttk.Button(frame, text="Iniciar sesión como Usuario", width=30, command=lambda: login(root, "usuarios")).pack(pady=5)
    ttk.Button(frame, text="Iniciar sesión como Admin", width=30, command=lambda: login(root, "admin")).pack(pady=5)
    ttk.Button(frame, text="Registrar Usuario", width=30, command=lambda: nuevo_usuario(root)).pack(pady=5)
    ttk.Button(frame, text="Registrar Administrador", width=30, command=lambda: nuevo_admin(root)).pack(pady=5)
    ttk.Button(frame, text="Salir", width=30, command=root.quit).pack(pady=20)

if __name__ == "__main__":
    # Iniciar el servidor Flask en un hilo diferente para que no bloquee la interfaz gráfica
    def run_flask():
        app.run(host='0.0.0.0', port=5000)

    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Iniciar la interfaz gráfica de Tkinter
    root = tk.Tk()
    root.title("HomeKeep")
    root.geometry("500x800")
    root.configure(bg="#000068")
    pantalla_inicio(root)
    root.mainloop()
