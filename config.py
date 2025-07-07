# config.py
import mysql.connector

def conectar_bd():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="homekeep_db"
        )
    except mysql.connector.Error as err:
        print(f"Error al conectar: {err}")
        return None
