# ver_usuarios.py actualizado con botón "Ver Información del Usuario"
import tkinter as tk
from tkinter import ttk, messagebox
from config import conectar_bd
from PIL import Image, ImageTk
from ver_info_usuario import ver_info_usuario  # ✅ nuevo

def ver_usuarios(root):
    ventana = tk.Toplevel(root)
    ventana.title("Usuarios Registrados")
    ventana.geometry("700x500")
    ventana.configure(bg="#E6F0FA")

    try:
        logo = Image.open("logotipo.jpg")
        logo = logo.resize((80, 80))
        logo_tk = ImageTk.PhotoImage(logo)
        label_logo = ttk.Label(ventana, image=logo_tk)
        label_logo.image = logo_tk
        label_logo.pack(pady=5)
    except:
        pass

    ttk.Label(ventana, text="Buscar usuario por ID:", font=("Arial", 11)).pack(pady=2)
    buscar_id = tk.StringVar()
    frame_buscar = ttk.Frame(ventana)
    frame_buscar.pack(pady=5)

    entry_buscar = ttk.Entry(frame_buscar, textvariable=buscar_id, width=30)
    entry_buscar.pack(side="left", padx=5)

    def buscar_usuario():
        for i in tree.get_children():
            tree.delete(i)
        id_valor = buscar_id.get().strip()
        conn = conectar_bd()
        if conn:
            cur = conn.cursor()
            if id_valor:
                cur.execute("SELECT id, nombre, contrasena, correo, telefono FROM usuarios WHERE id = %s", (id_valor,))
            else:
                cur.execute("SELECT id, nombre, contrasena, correo, telefono FROM usuarios")
            for fila in cur.fetchall():
                tree.insert("", "end", values=fila)
            conn.close()

    ttk.Button(frame_buscar, text="Buscar", command=buscar_usuario).pack(side="left")

    ttk.Label(ventana, text="Lista de Usuarios Registrados", font=("Arial", 14, "bold")).pack(pady=10)

    frame = ttk.Frame(ventana)
    frame.pack(fill="both", expand=True, padx=10)

    tree = ttk.Treeview(frame, columns=("ID", "Nombre", "Contraseña", "Correo", "Teléfono"), show="headings")
    for col in ("ID", "Nombre", "Contraseña", "Correo", "Teléfono"):
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(fill="both", expand=True)

    def cargar_usuarios():
        for i in tree.get_children():
            tree.delete(i)
        conn = conectar_bd()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT id, nombre, contrasena, correo, telefono FROM usuarios")
            for fila in cur.fetchall():
                tree.insert("", "end", values=fila)
            conn.close()

    def eliminar_usuario():
        item = tree.selection()
        if item:
            datos = tree.item(item[0])["values"]
            usuario_id = datos[0]
            confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar al usuario con ID {usuario_id}?")
            if confirmar:
                conn = conectar_bd()
                if conn:
                    cur = conn.cursor()
                    cur.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
                    conn.commit()
                    conn.close()
                    cargar_usuarios()
                    messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
        else:
            messagebox.showwarning("Selecciona uno", "Debes seleccionar un usuario para eliminar.")

    def abrir_info_usuario():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Selecciona uno", "Selecciona un usuario para ver su información.")
            return
        datos = tree.item(item[0])["values"]
        usuario_id = datos[0]
        usuario_nombre = datos[1]
        ver_info_usuario(ventana, usuario_id, usuario_nombre)

    # BOTONES
    boton_frame = ttk.Frame(ventana)
    boton_frame.pack(pady=10)

    ttk.Button(boton_frame, text="Ver Información del Usuario", command=abrir_info_usuario).pack(side="left", padx=10)
    ttk.Button(boton_frame, text="Eliminar Usuario Seleccionado", command=eliminar_usuario).pack(side="left", padx=10)
    ttk.Button(boton_frame, text="Cerrar", command=ventana.destroy).pack(side="left", padx=10)

    cargar_usuarios()
