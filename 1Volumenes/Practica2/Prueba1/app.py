import os, datetime, pathlib, sys
DATA_DIR = "/data"
pathlib.Path(DATA_DIR).mkdir(parents=True, exist_ok=True)

mensaje = os.getenv("MENSAJE", "Nota por defecto")
nota = f"[{datetime.datetime.now().isoformat()}] {mensaje}\n"

with open(f"{DATA_DIR}/notas.txt", "a", encoding="utf-8") as f:
    f.write(nota)

print("Nota agregada. Contenido actual de notas.txt:")
with open(f"{DATA_DIR}/notas.txt", "r", encoding="utf-8") as f:
    sys.stdout.write(f.read())
