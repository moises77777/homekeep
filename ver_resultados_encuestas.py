# ver_resultados_encuestas.py actualizado
import tkinter as tk
from tkinter import ttk
from config import conectar_bd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def ver_resultados_encuestas(root):
    ventana = tk.Toplevel(root)
    ventana.title("Resultados de Encuestas")
    ventana.geometry("600x500")
    ventana.configure(bg="#F0F8FF")

    ttk.Label(ventana, text="Resultados de Encuestas (Gráfica de Pastel)", font=("Arial", 14, "bold")).pack(pady=10)

    conn = conectar_bd()
    datos = {"Excelente": 0, "Buena": 0, "Regular": 0, "Mala": 0}
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT respuesta FROM respuestas_encuesta")
        resultados = cur.fetchall()
        for r in resultados:
            val = r[0].capitalize()
            if val in datos:
                datos[val] += 1
        conn.close()

    total = sum(datos.values())
    if total == 0:
        ttk.Label(ventana, text="No hay datos suficientes para mostrar la gráfica.").pack(pady=20)
        return

    fig = Figure(figsize=(5, 4))
    ax = fig.add_subplot(111)
    etiquetas = [f"{k} ({v})" for k, v in datos.items()]
    valores = list(datos.values())

    ax.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90)
    ax.set_title("Satisfacción Global")

    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)

    ttk.Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)
