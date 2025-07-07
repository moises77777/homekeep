# ver_encuestas.py
import tkinter as tk
from tkinter import ttk, messagebox
from config import conectar_bd
import matplotlib.pyplot as plt

def ver_encuestas(root):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT respuesta, COUNT(*) FROM encuestas GROUP BY respuesta")
            datos = cursor.fetchall()

            if datos:
                respuestas = [fila[0] for fila in datos]
                cantidades = [fila[1] for fila in datos]

                plt.figure(figsize=(6, 4))
                plt.bar(respuestas, cantidades)
                plt.title("Resultados de Encuesta de Satisfacción")
                plt.xlabel("Respuesta")
                plt.ylabel("Cantidad de votos")
                plt.tight_layout()
                plt.show()
            else:
                messagebox.showinfo("Sin datos", "No hay encuestas registradas.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener los datos:\n{e}")
        finally:
            cursor.close()
            conexion.close()
