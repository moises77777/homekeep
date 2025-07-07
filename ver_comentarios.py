# ver_comentarios.py actualizado para tabla comentarios_encuesta
import tkinter as tk
from tkinter import ttk, messagebox
from config import conectar_bd

def ver_comentarios_encuestas(root):
    ventana = tk.Toplevel(root)
    ventana.title("Comentarios de Encuestas")
    ventana.geometry("500x400")
    ventana.configure(bg="#F0F8FF")

    ttk.Label(ventana, text="Comentarios Recibidos", font=("Arial", 14, "bold")).pack(pady=10)

    frame = ttk.Frame(ventana)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    texto = tk.Text(frame, wrap="word", height=15, width=60)
    texto.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=texto.yview)
    scrollbar.pack(side="right", fill="y")
    texto.config(yscrollcommand=scrollbar.set)

    conn = conectar_bd()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT comentario FROM comentarios_encuesta WHERE comentario IS NOT NULL AND comentario != ''")
            resultados = cur.fetchall()
            if resultados:
                for row in resultados:
                    texto.insert("end", f"• {row[0]}\n\n")
            else:
                texto.insert("end", "No hay comentarios disponibles.")
        except Exception as e:
            texto.insert("end", f"Error al obtener comentarios: {str(e)}")
        finally:
            conn.close()
    else:
        texto.insert("end", "Error al conectar con la base de datos.")

    ttk.Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)
