# ver_estadisticas.py
import tkinter as tk
from tkinter import ttk
from config import conectar_bd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def ver_estadisticas(root):
    ventana = tk.Toplevel(root)
    ventana.title("Estadísticas del Sistema")
    ventana.geometry("800x600")
    ventana.configure(bg="#F0F8FF")

    ttk.Label(ventana, text="Estadísticas Generales", font=("Arial", 16, "bold")).pack(pady=10)

    conn = conectar_bd()
    if not conn:
        ttk.Label(ventana, text="No se pudo conectar a la base de datos.").pack()
        return

    cursor = conn.cursor()

    try:
        # TOTAL DE USUARIOS
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total_usuarios = cursor.fetchone()[0]

        # TOTAL DE SOLICITUDES
        cursor.execute("SELECT COUNT(*) FROM solicitudes")
        total_solicitudes = cursor.fetchone()[0]

        ttk.Label(ventana, text=f"Usuarios registrados: {total_usuarios}", font=("Arial", 12)).pack()
        ttk.Label(ventana, text=f"Solicitudes registradas: {total_solicitudes}", font=("Arial", 12)).pack(pady=10)

        # SOLICITUDES POR ESTADO
        cursor.execute("SELECT estado, COUNT(*) FROM solicitudes GROUP BY estado")
        estado_data = cursor.fetchall()

        # SOLICITUDES POR GRAVEDAD
        cursor.execute("SELECT gravedad, COUNT(*) FROM solicitudes GROUP BY gravedad")
        gravedad_data = cursor.fetchall()

        conn.close()

        # GRAFICAR ESTADO
        if estado_data:
            fig1 = Figure(figsize=(4, 3))
            ax1 = fig1.add_subplot(111)
            estados = [row[0] for row in estado_data]
            cantidades = [row[1] for row in estado_data]
            ax1.bar(estados, cantidades, color="steelblue")
            ax1.set_title("Solicitudes por Estado")
            ax1.set_ylabel("Cantidad")

            canvas1 = FigureCanvasTkAgg(fig1, master=ventana)
            canvas1.draw()
            canvas1.get_tk_widget().pack(pady=10)

        # GRAFICAR GRAVEDAD
        if gravedad_data:
            fig2 = Figure(figsize=(4, 3))
            ax2 = fig2.add_subplot(111)
            etiquetas = [row[0] for row in gravedad_data]
            valores = [row[1] for row in gravedad_data]
            ax2.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90)
            ax2.set_title("Distribución por Gravedad")

            canvas2 = FigureCanvasTkAgg(fig2, master=ventana)
            canvas2.draw()
            canvas2.get_tk_widget().pack(pady=10)

    except Exception as e:
        ttk.Label(ventana, text=f"Error al obtener estadísticas: {e}").pack(pady=10)

    ttk.Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)
