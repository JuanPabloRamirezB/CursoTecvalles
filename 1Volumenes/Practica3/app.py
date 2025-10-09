import os, pathlib, time

CACHE_DIR = "/cache"
pathlib.Path(CACHE_DIR).mkdir(parents=True, exist_ok=True)

for i in range(3):
    with open(f"{CACHE_DIR}/chunk_{i}.bin", "wb") as f:
        f.write(os.urandom(256 * 1024))
    print(f"Escrito chunk_{i}.bin en tmpfs")

print("\n Contenido en /cache:")
print("\n".join(sorted(os.listdir(CACHE_DIR))))

FILE_TO_INSPECT = f"{CACHE_DIR}/chunk_0.bin"

try:
    with open(FILE_TO_INSPECT, "rb") as f:
        data = f.read(20)
    
    print(f"\n Primeros 20 bytes de {os.path.basename(FILE_TO_INSPECT)} (Hexadecimal):")
    print(data.hex())
    
except FileNotFoundError:
    print(f"\n[ERROR] No se encontró el archivo: {FILE_TO_INSPECT}")

print("\n Esperando 2s…")
time.sleep(2)
print("Fin. Recuerda: estos archivos viven en RAM y se pierden al parar el contenedor.")
