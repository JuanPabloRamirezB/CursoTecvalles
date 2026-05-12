from flask import Flask
import os
import threading
 
app = Flask(__name__)
ARCHIVO = '/data/contador.txt'
lock = threading.Lock()   # evita race conditions entre requests concurrentes
 
def leer_contador():
    if not os.path.exists(ARCHIVO):
        return 0
    with open(ARCHIVO, 'r') as f:
        contenido = f.read().strip()
        return int(contenido) if contenido else 0
 
def guardar_contador(n):
    os.makedirs(os.path.dirname(ARCHIVO), exist_ok=True)
    with open(ARCHIVO, 'w') as f:
        f.write(str(n))
 
@app.route('/')
def index():
    with lock:
        n = leer_contador() + 1
        guardar_contador(n)
    return f"Saludos desde el dispositivo de JP.\n"\
           f"Esta página ha sido visitada {n} veces.\n"
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
