# admin_encuestas.py FINAL
import tkinter as tk
from tkinter import ttk, messagebox
from config import conectar_bd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def admin_encuestas(root):
    win = tk.Toplevel(root)
    win.title("Administrar Encuestas")
    win.geometry("900x700")
    win.configure(bg="#F0F8FF")

    ttk.Label(win, text="Gestión de Encuestas", font=("Arial", 16, "bold")).pack(pady=10)

    # ==== GRÁFICA DE SATISFACCIÓN ====
    frame_grafica = ttk.LabelFrame(win, text="Gráfica de Satisfacción General", padding=10)
    frame_grafica.pack(fill="x", padx=20, pady=10)

    def cargar_grafica():
        datos = {"Excelente": 0, "Buena": 0, "Regular": 0, "Mala": 0}
        conn = conectar_bd()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT respuesta FROM respuestas_encuesta")
                for r in cur.fetchall():
                    val = r[0].capitalize()
                    if val in datos:
                        datos[val] += 1
                cur.close()
                conn.close()
            except:
                pass

        total = sum(datos.values())
        if total == 0:
            ttk.Label(frame_grafica, text="Sin datos suficientes para mostrar.", foreground="red").pack()
            return

        fig = Figure(figsize=(4, 3))
        ax = fig.add_subplot(111)
        etiquetas = [f"{k} ({v})" for k, v in datos.items()]
        valores = list(datos.values())

        ax.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90)
        ax.set_title("Satisfacción General")

        canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
        canvas.draw()
        canvas.get_tk_widget().pack()

    cargar_grafica()

    # ==== COMENTARIOS ====
    frame_coment = ttk.LabelFrame(win, text="Comentarios Recibidos", padding=10)
    frame_coment.pack(fill="x", padx=20, pady=10)

    comentarios_box = tk.Listbox(frame_coment, height=6, width=80)
    comentarios_box.pack(pady=5)

    def cargar_comentarios():
        comentarios_box.delete(0, "end")
        conn = conectar_bd()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT id, comentario FROM comentarios_encuesta WHERE comentario IS NOT NULL AND comentario != ''")
                for row in cur.fetchall():
                    comentarios_box.insert("end", f"{row[0]} - {row[1][:70]}")
                cur.close()
                conn.close()
            except:
                comentarios_box.insert("end", "Error al cargar comentarios.")

    def eliminar_comentario():
        seleccionado = comentarios_box.curselection()
        if not seleccionado:
            messagebox.showwarning("Selecciona", "Selecciona un comentario para eliminar.")
            return
        valor = comentarios_box.get(seleccionado)
        id_comentario = valor.split(" - ")[0]

        conn = conectar_bd()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM comentarios_encuesta WHERE id = %s", (id_comentario,))
                conn.commit()
                conn.close()
                cargar_comentarios()
                messagebox.showinfo("Listo", "Comentario eliminado.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    ttk.Button(frame_coment, text="Eliminar Comentario Seleccionado", command=eliminar_comentario).pack()

    cargar_comentarios()

    # ==== PREGUNTAS DE ENCUESTA ====
    frame_preg = ttk.LabelFrame(win, text="Preguntas de la Encuesta", padding=10)
    frame_preg.pack(fill="both", padx=20, pady=10, expand=True)

    tabla = ttk.Treeview(frame_preg, columns=("ID", "Pregunta"), show="headings", height=5)
    tabla.heading("ID", text="ID")
    tabla.heading("Pregunta", text="Texto de la Pregunta")
    tabla.column("ID", width=40)
    tabla.column("Pregunta", width=500)
    tabla.pack(pady=5, fill="both", expand=True)

    def cargar_preguntas():
        for i in tabla.get_children():
            tabla.delete(i)
        conn = conectar_bd()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT id, texto FROM preguntas")
                for row in cur.fetchall():
                    tabla.insert("", "end", values=row)
                cur.close()
                conn.close()
            except:
                messagebox.showerror("Error", "No se pudieron cargar las preguntas.")

    def agregar_pregunta():
        texto = entry_preg.get().strip()
        if not texto:
            messagebox.showwarning("Atención", "Escribe una pregunta.")
            return
        conn = conectar_bd()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("INSERT INTO preguntas (texto) VALUES (%s)", (texto,))
                conn.commit()
                conn.close()
                entry_preg.delete(0, "end")
                cargar_preguntas()
                messagebox.showinfo("Agregado", "Pregunta agregada.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar: {e}")

    def eliminar_pregunta():
        item = tabla.selection()
        if not item:
            messagebox.showwarning("Selecciona", "Selecciona una pregunta.")
            return
        pid = tabla.item(item[0])["values"][0]
        conn = conectar_bd()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM preguntas WHERE id = %s", (pid,))
                conn.commit()
                conn.close()
                cargar_preguntas()
                messagebox.showinfo("Eliminado", "Pregunta eliminada.")
            except Exception as e:
                messagebox.showerror("Error", "No se pudo eliminar.")

    # === FORMULARIO DE BOTONES Y ENTRADA ===
    frame_form = ttk.LabelFrame(win, text="Agregar o Eliminar Pregunta", padding=10)
    frame_form.pack(fill="x", padx=20, pady=5)

    entry_preg = ttk.Entry(frame_form, width=80)
    entry_preg.grid(row=0, column=0, padx=10, pady=5)

    ttk.Button(frame_form, text="Agregar Pregunta", command=agregar_pregunta).grid(row=0, column=1, padx=5)
    ttk.Button(frame_form, text="Eliminar Pregunta Seleccionada", command=eliminar_pregunta).grid(row=0, column=2, padx=5)

    cargar_preguntas()

    ttk.Button(win, text="Cerrar", command=win.destroy).pack(pady=10)
