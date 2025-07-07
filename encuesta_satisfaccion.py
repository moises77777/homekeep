# encuesta_satisfaccion.py dinámico final
import tkinter as tk
from tkinter import messagebox
from config import conectar_bd
from datetime import datetime

def encuesta_satisfaccion(root, usuario):
    ventana = tk.Toplevel(root)
    ventana.title("Encuesta de Satisfacción")
    ventana.geometry("500x600")
    ventana.configure(bg="#F0F8FF")

    tk.Label(ventana, text="Encuesta de Satisfacción", font=("Arial", 16, "bold"), bg="#F0F8FF").pack(pady=10)

    marco_preguntas = tk.Frame(ventana, bg="#F0F8FF")
    marco_preguntas.pack(pady=5, fill="both", expand=True)

    respuestas = {}  # Diccionario {pregunta_id: variable_seleccionada}

    conn = conectar_bd()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, texto FROM preguntas")
            preguntas = cur.fetchall()

            if not preguntas:
                tk.Label(marco_preguntas, text="No hay preguntas configuradas.", bg="#F0F8FF").pack(pady=10)
                return

            for pid, texto in preguntas:
                tk.Label(marco_preguntas, text=texto, bg="#F0F8FF", anchor="w", justify="left", wraplength=400, font=("Arial", 10, "bold")).pack(anchor="w", padx=20, pady=2)
                var = tk.StringVar()
                respuestas[pid] = var
                for opcion in ["Excelente", "Buena", "Regular", "Mala"]:
                    tk.Radiobutton(marco_preguntas, text=opcion, variable=var, value=opcion, bg="#F0F8FF").pack(anchor="w", padx=40)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las preguntas:\n{e}")
            return
        finally:
            conn.close()
    else:
        tk.Label(marco_preguntas, text="No se pudo conectar a la base de datos.", bg="#F0F8FF").pack()

    # Comentarios
    tk.Label(ventana, text="Comentario general (opcional):", bg="#F0F8FF").pack(pady=(10, 0))
    comentario_txt = tk.Text(ventana, height=4, width=50)
    comentario_txt.pack(pady=5)

    def enviar():
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        comentario = comentario_txt.get("1.0", "end").strip()

        # Validar que todas las preguntas tengan respuesta
        for pid, var in respuestas.items():
            if not var.get():
                messagebox.showwarning("Incompleto", "Por favor responde todas las preguntas.")
                return

        conn = conectar_bd()
        if conn:
            try:
                cur = conn.cursor()
                for pid, var in respuestas.items():
                    cur.execute("""
                        INSERT INTO respuestas_encuesta (usuario_nombre, pregunta_id, respuesta, fecha)
                        VALUES (%s, %s, %s, %s)
                    """, (usuario, pid, var.get(), fecha))

                if comentario:
                    cur.execute("""
                        INSERT INTO comentarios_encuesta (usuario_nombre, comentario, fecha)
                        VALUES (%s, %s, %s)
                    """, (usuario, comentario, fecha))

                conn.commit()
                messagebox.showinfo("Gracias", "Tus respuestas han sido registradas.")
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudieron guardar las respuestas:\n{e}")
            finally:
                conn.close()

    tk.Button(ventana, text="Enviar Encuesta", command=enviar).pack(pady=10)
    tk.Button(ventana, text="Cancelar", command=ventana.destroy).pack()
