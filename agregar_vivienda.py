# agregar_vivienda.py completo (registrar, ver, editar, eliminar)
import tkinter as tk
from tkinter import ttk, messagebox
from config import conectar_bd

def agregar_vivienda(root, usuario):
    win = tk.Toplevel(root)
    win.title("Gestión de Viviendas")
    win.geometry("800x600")
    win.configure(bg="#E6F0FA")

    # --- FORMULARIO DE REGISTRO ---
    ttk.Label(win, text="Registrar Nueva Vivienda", font=("Arial", 14, "bold")).pack(pady=5)

    frame_form = ttk.Frame(win)
    frame_form.pack(pady=10)

    campos = {
        "Municipio": tk.StringVar(),
        "Localidad": tk.StringVar(),
        "Calle": tk.StringVar(),
        "Número": tk.StringVar(),
        "Tipo de Vivienda": tk.StringVar()
    }

    for idx, (label, var) in enumerate(campos.items()):
        ttk.Label(frame_form, text=label).grid(row=idx, column=0, sticky="e", padx=5, pady=2)
        ttk.Entry(frame_form, textvariable=var).grid(row=idx, column=1, padx=5, pady=2)

    def registrar():
        datos = {k: v.get().strip() for k, v in campos.items()}
        if not all(datos.values()):
            messagebox.showwarning("Campos vacíos", "Completa todos los campos.")
            return

        conn = conectar_bd()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO viviendas (municipio, localidad, calle, numero, tipo_vivienda, usuario_nombre)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    datos["Municipio"], datos["Localidad"], datos["Calle"],
                    datos["Número"], datos["Tipo de Vivienda"], usuario
                ))
                conn.commit()
                messagebox.showinfo("Éxito", "Vivienda registrada.")
                cargar_viviendas()
                for v in campos.values():
                    v.set("")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

    ttk.Button(frame_form, text="Registrar Vivienda", command=registrar).grid(columnspan=2, pady=10)

    # --- TABLA DE VIVIENDAS ---
    ttk.Label(win, text="Mis Viviendas Registradas", font=("Arial", 13, "bold")).pack(pady=5)
    frame_tabla = ttk.Frame(win)
    frame_tabla.pack(fill="both", expand=True, padx=10)

    tabla = ttk.Treeview(frame_tabla, columns=("ID", "Municipio", "Localidad", "Calle", "Número", "Tipo"), show="headings")
    for col in tabla["columns"]:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)
    tabla.pack(fill="both", expand=True)

    # --- FUNCIONES DE EDITAR Y ELIMINAR ---
    def cargar_viviendas():
        for i in tabla.get_children():
            tabla.delete(i)
        conn = conectar_bd()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT id, municipio, localidad, calle, numero, tipo_vivienda FROM viviendas WHERE usuario_nombre = %s", (usuario,))
                for fila in cur.fetchall():
                    tabla.insert("", "end", values=fila)
            except Exception as e:
                messagebox.showerror("Error al cargar viviendas", str(e))
            finally:
                conn.close()

    def editar_vivienda():
        item = tabla.selection()
        if not item:
            messagebox.showwarning("Selecciona", "Selecciona una vivienda para editar.")
            return
        datos = tabla.item(item[0])["values"]
        id_viv = datos[0]

        for idx, key in enumerate(campos.keys()):
            campos[key].set(datos[idx+1])  # +1 para saltar el ID

        def actualizar():
            nuevos = {k: v.get().strip() for k, v in campos.items()}
            if not all(nuevos.values()):
                messagebox.showwarning("Campos vacíos", "Completa todos los campos.")
                return
            conn = conectar_bd()
            if conn:
                try:
                    cur = conn.cursor()
                    cur.execute("""
                        UPDATE viviendas SET municipio=%s, localidad=%s, calle=%s, numero=%s, tipo_vivienda=%s
                        WHERE id = %s AND usuario_nombre = %s
                    """, (
                        nuevos["Municipio"], nuevos["Localidad"], nuevos["Calle"],
                        nuevos["Número"], nuevos["Tipo de Vivienda"], id_viv, usuario
                    ))
                    conn.commit()
                    messagebox.showinfo("Éxito", "Vivienda actualizada.")
                    cargar_viviendas()
                    for v in campos.values():
                        v.set("")
                except Exception as e:
                    messagebox.showerror("Error al actualizar", str(e))
                finally:
                    conn.close()

        ttk.Button(frame_form, text="Guardar Cambios", command=actualizar).grid(columnspan=2, pady=5)

    def eliminar_vivienda():
        item = tabla.selection()
        if not item:
            messagebox.showwarning("Selecciona", "Selecciona una vivienda para eliminar.")
            return
        datos = tabla.item(item[0])["values"]
        id_viv = datos[0]

        confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar la vivienda ID {id_viv}?")
        if confirmar:
            conn = conectar_bd()
            if conn:
                try:
                    cur = conn.cursor()
                    cur.execute("DELETE FROM viviendas WHERE id = %s AND usuario_nombre = %s", (id_viv, usuario))
                    conn.commit()
                    cargar_viviendas()
                    messagebox.showinfo("Eliminada", "Vivienda eliminada correctamente.")
                except Exception as e:
                    messagebox.showerror("Error al eliminar", str(e))
                finally:
                    conn.close()

    ttk.Button(win, text="Editar Vivienda Seleccionada", command=editar_vivienda).pack(pady=5)
    ttk.Button(win, text="Eliminar Vivienda Seleccionada", command=eliminar_vivienda).pack(pady=5)
    ttk.Button(win, text="Cerrar", command=win.destroy).pack(pady=10)

    cargar_viviendas()
