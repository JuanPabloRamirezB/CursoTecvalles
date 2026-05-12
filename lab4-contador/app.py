# app.py — Versión 3: contador en Redis
from flask import Flask
from redis import Redis
import os
 
app = Flask(__name__)
redis_host = os.environ.get('REDIS_HOST', 'redis')
redis_port = int(os.environ.get('REDIS_PORT', 6379))
cache = Redis(host=redis_host, port=redis_port, decode_responses=True)
 
@app.route('/')
def index():
    n = cache.incr('visitas')
    return f"Saludos desde el dispositivo de JP.\n"\
           f"Esta página ha sido visitada {n} veces.\n"
 
@app.route('/reset')
def reset():
    cache.set('visitas', 0)
    return "Contador reiniciado.\n"
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
