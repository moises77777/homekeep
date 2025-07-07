import mysql.connector
from pymongo import MongoClient

# Conexión a MySQL
mysql_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="homekeep_db"
)

# Conexión a MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["homekeep_db_mongo"]

# Listado de tablas que deseas migrar
tablas = ["usuarios", "admin", "solicitudes", "viviendas", "recordatorios", "encuestas"]

cursor = mysql_conn.cursor(dictionary=True)

for tabla in tablas:
    cursor.execute(f"SELECT * FROM {tabla}")
    filas = cursor.fetchall()
    if filas:
        mongo_db[tabla].insert_many(filas)
        print(f"✅ Migrados {len(filas)} registros de '{tabla}' a MongoDB")
    else:
        print(f"⚠️ Tabla '{tabla}' está vacía.")

cursor.close()
mysql_conn.close()
print("✅ Migración completa.")
