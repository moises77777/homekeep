# ver_info_usuario.py
import tkinter as tk
from tkinter import ttk, messagebox
from config import conectar_bd

def ver_info_usuario(root, usuario_id, usuario_nombre):
    win = tk.Toplevel(root)
    win.title(f"Información de {usuario_nombre}")
    win.geometry("800x600")
    win.configure(bg="#E6F0FA")

    ttk.Label(win, text=f"Información completa del usuario: {usuario_nombre}",
              font=("Arial", 16, "bold")).pack(pady=10)

    conn = conectar_bd()
    if not conn:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cur = conn.cursor()

        # --- DATOS PERSONALES ---
        ttk.Label(win, text="Datos del Usuario", font=("Arial", 13, "bold")).pack(anchor="w", padx=15)
        cur.execute("SELECT nombre, correo, telefono FROM usuarios WHERE id = %s", (usuario_id,))
        datos = cur.fetchone()
        if datos:
            nombre, correo, telefono = datos
            ttk.Label(win, text=f"Nombre: {nombre}").pack(anchor="w", padx=30)
            ttk.Label(win, text=f"Correo: {correo}").pack(anchor="w", padx=30)
            ttk.Label(win, text=f"Teléfono: {telefono}").pack(anchor="w", padx=30)
        else:
            ttk.Label(win, text="Usuario no encontrado.").pack()

        # --- VIVIENDAS ---
        ttk.Label(win, text="Viviendas Registradas", font=("Arial", 13, "bold")).pack(anchor="w", padx=15, pady=(10, 0))
        cur.execute("SELECT municipio, localidad, calle, numero, tipo_vivienda FROM viviendas WHERE usuario_nombre = %s", (usuario_nombre,))
        viviendas = cur.fetchall()
        if viviendas:
            for viv in viviendas:
                ttk.Label(win, text=f"- {viv[0]}, {viv[1]}, {viv[2]} #{viv[3]} ({viv[4]})").pack(anchor="w", padx=30)
        else:
            ttk.Label(win, text="No tiene viviendas registradas.").pack(anchor="w", padx=30)

        # --- SOLICITUDES ---
        ttk.Label(win, text="Solicitudes", font=("Arial", 13, "bold")).pack(anchor="w", padx=15, pady=(10, 0))
        cur.execute("SELECT titulo, estado, gravedad FROM solicitudes WHERE usuario_nombre = %s", (usuario_nombre,))
        solicitudes = cur.fetchall()
        if solicitudes:
            for sol in solicitudes:
                ttk.Label(win, text=f"- [{sol[1]} - {sol[2]}] {sol[0]}").pack(anchor="w", padx=30)
        else:
            ttk.Label(win, text="No ha enviado solicitudes.").pack(anchor="w", padx=30)

        # --- RECORDATORIOS ---
        ttk.Label(win, text="Recordatorios", font=("Arial", 13, "bold")).pack(anchor="w", padx=15, pady=(10, 0))
        cur.execute("SELECT titulo, mensaje FROM recordatorios WHERE usuario_nombre = %s", (usuario_nombre,))
        recordatorios = cur.fetchall()
        if recordatorios:
            for r in recordatorios:
                ttk.Label(win, text=f"- {r[0]}: {r[1]}").pack(anchor="w", padx=30)
        else:
            ttk.Label(win, text="No tiene recordatorios.").pack(anchor="w", padx=30)

        # --- ENCUESTAS ---
        ttk.Label(win, text="Encuestas", font=("Arial", 13, "bold")).pack(anchor="w", padx=15, pady=(10, 0))
        cur.execute("SELECT satisfaccion_general, tiempo_respuesta, trato_personal FROM encuestas WHERE usuario_nombre = %s", (usuario_nombre,))
        encuestas = cur.fetchall()
        if encuestas:
            for e in encuestas:
                ttk.Label(win, text=f"- {e[0]} / {e[1]} / {e[2]}").pack(anchor="w", padx=30)
        else:
            ttk.Label(win, text="No ha contestado encuestas.").pack(anchor="w", padx=30)

    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()

    ttk.Button(win, text="Cerrar", command=win.destroy).pack(pady=15)
