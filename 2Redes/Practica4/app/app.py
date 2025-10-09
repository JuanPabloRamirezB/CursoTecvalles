from flask import Flask, jsonify, request
import psycopg2, os, time
from decimal import Decimal

app = Flask(__name__)

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "secret")
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "tienda")

def get_conn():
    return psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

def crear_tabla():
    # reintenta conexión por si Postgres aún no está listo
    for i in range(20):
        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS productos (
                            id SERIAL PRIMARY KEY,
                            nombre TEXT NOT NULL,
                            precio NUMERIC
                        );
                    """)
                conn.commit()
            print("DB lista y tabla creada/validada.")
            return
        except Exception as e:
            print(f"DB no lista aún ({i+1}/20): {e}")
            time.sleep(1)
    # si no logró conectar, dejamos que falle para verlo en logs
    with get_conn() as conn:
        pass

@app.get("/")
def health():
    return "OK", 200

@app.get("/listarproductos")
def listar():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, nombre, precio FROM productos;")
            filas = cur.fetchall()
    data = [
        {"id": r[0], "nombre": r[1],
         "precio": float(r[2]) if isinstance(r[2], (Decimal, float)) and r[2] is not None else None}
        for r in filas
    ]
    return jsonify(data), 200

@app.post("/anadirproductos")
def agregar():
    data = request.get_json(force=True, silent=True) or {}
    nombre = data.get("nombre")
    precio = data.get("precio")
    if not nombre or precio is None:
        return jsonify(error='Formato: {"nombre": str, "precio": number}'), 400
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO productos (nombre, precio) VALUES (%s, %s);", (nombre, precio))
        conn.commit()
    return jsonify({"nombre": nombre, "precio": float(precio)}), 201

# crear tabla al arrancar
crear_tabla()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
