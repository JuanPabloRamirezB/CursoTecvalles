from flask import Flask
 
app = Flask(__name__)
visitas = 0   # variable global en memoria del proceso
 
@app.route('/')
def index():
    global visitas
    visitas += 1
    return f"Saludos desde el dispositivo de JP.\n"\
    f"Esta página ha sido visitada {visitas} veces.\n"
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
