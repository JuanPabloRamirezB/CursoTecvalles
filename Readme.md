# Taller de Virtualización y Contenedores — Parte Práctica

---

## Lab 0 — Verificación del entorno

**Mapea a:** Slide 2 (contexto computacional)

**Objetivo:** Confirmar que todos los participantes tienen el entorno listo antes de empezar.

### Pasos

1. Abre una terminal en tu sistema.  
     
2. Verifica versiones:  
     ``` bash
   docker \--version  
     
   docker compose version  
   ```
     
     
3. Comprueba que Docker está corriendo:  
     ``` bash
   docker run hello-world  
     ```


## Lab 1 — Primer contenedor: aislamiento y ligereza

**Mapea a:** Slides 15, 16, 17, 20 (qué es un contenedor, motores, Docker)

**Objetivo:** Contrastar el peso de una VM contra un contenedor. Entender procesos aislados.

### Pasos

1. Verifica la información del motor Docker:  
     ``` bash
   docker info  
   ```

     
   Identifica: Server Version, Storage Driver, Total Memory, Operating System.  
     
2. Corre un contenedor interactivo:  
     
   ``` bash
   docker run -it --rm --name explorador ubuntu bash  
   ```

     
   Dentro del contenedor:  
   ``` bash
   cat /etc/os-release  
     
   ps aux  
     
   ls /  
     
   whoami  
   ```
     
3. **En OTRA terminal del host**, ejecuta:  
   
   ```bahs
   docker ps  
     
   ps aux | grep \-v grep | grep bash  
   ```

     
4. Sal del contenedor (`exit`) y observa que ya no aparece en `docker ps`. Aparece en `docker ps -a` con estado `Exited`.  
     
5. Corre un servicio real:  
     ``` bash
   docker run -d --name web -p 8080:80 nginx  
     
   curl http://localhost:8080  
     
   docker logs web  
     
   docker exec -it web bash  
   ```
     
   Dentro: `cat /etc/nginx/nginx.conf`, `nginx -v`, luego `exit`.  
     
6. Limpia:  
     ``` bash
   docker stop web  
     
   docker rm web  
     
   docker ps \-a
   ```

---

## Lab 2 — Tu primera imagen: contador en memoria
 
**Mapea a:** Slides 19, 20 (arquitectura de contenedores, imágenes OCI)
 
**Objetivo:** Construir una imagen propia desde un `Dockerfile`. Entender capas. Descubrir, en carne propia, por qué los contenedores son efímeros.
 
### Paso 1 — Explora una imagen existente
 
```bash
docker images
docker history nginx
```
 
Observa: cada `RUN`, `COPY`, `ADD` produjo una capa. Las capas se comparten entre imágenes — si dos imágenes usan `python:3.12-alpine` como base, Docker no descarga esa capa dos veces.
 
### Paso 2 — Prepara la carpeta del proyecto
 
```bash
mkdir lab2-contador && cd lab2-contador
```
 
### Paso 3 — Crea `app.py`
 
Esta es la **versión 1** del contador. Guarda el número de visitas en una variable global de Python que vive en memoria del proceso.
 
```python
# app.py — Versión 1: contador en memoria
from flask import Flask
 
app = Flask(__name__)
visitas = 0   # variable global en memoria del proceso
 
@app.route('/')
def index():
    global visitas
    visitas += 1
    return f"Esta página ha sido visitada {visitas} veces.\n"
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```
 
### Paso 4 — Crea `requirements.txt`
 
```
flask
```
 
### Paso 5 — Crea el `Dockerfile`
 
```dockerfile
FROM python:3.12-alpine
WORKDIR /app
 
# Instalamos dependencias PRIMERO para aprovechar la caché:
# si app.py cambia, esta capa no se vuelve a construir.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
# El código de la app va al final porque cambia más seguido.
COPY app.py .
 
EXPOSE 5000
CMD ["python", "app.py"]
```
 
### Paso 6 — Construye la imagen
 
```bash
docker build -t contador:v1 .
docker images contador
docker history contador:v1
```
 
Observa el orden de las capas y cuánto pesa cada una.
 
### Paso 7 — Corre la app
 
```bash
docker run -d --name contador -p 5000:5000 contador:v1
 
curl http://localhost:5000
curl http://localhost:5000
curl http://localhost:5000
```
 
Cada visita incrementa el contador. Hasta aquí, todo perfecto.
 
### Paso 8 — El problema: matar el contenedor
 
```bash
docker rm -f contador
docker run -d --name contador -p 5000:5000 contador:v1
curl http://localhost:5000
```

---
 
## Lab 3 — Persistencia: contador en archivo
 
**Mapea a:** Slide 23 (volúmenes, bind mounts, tmpfs)
 
**Objetivo:** Resolver el problema del Lab 3. Aprender las tres formas de persistir datos: bind mount, volumen nombrado y tmpfs.
 
### Paso 1 — Reescribe la app (versión 2)
 
Modifica `app.py` para que guarde el contador en `/data/contador.txt`:
 
```python
# app.py — Versión 2: contador persistido en archivo
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
    return f"Esta página ha sido visitada {n} veces.\n"
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```
 
El `Dockerfile` y el `requirements.txt` se quedan igual. Reconstruye la imagen:
 
```bash
docker build -t contador:v2 .
```
 
### Paso 2 — Sin volumen: el problema sigue
 
```bash
docker run -d --name contador -p 5000:5000 contador:v2
curl http://localhost:5000
curl http://localhost:5000
docker rm -f contador
 
docker run -d --name contador -p 5000:5000 contador:v2
curl http://localhost:5000
```
 
Sigue volviendo a `1`. **¿Por qué?** Porque `/data/contador.txt` vive **dentro del contenedor**. Cuando lo matas con `docker rm -f`, el filesystem del contenedor también se elimina. Necesitamos guardar el archivo en algún lugar que sobreviva al contenedor.
 
### Paso 3 — Bind mount: ata una carpeta del host
 
```bash
docker rm -f contador
mkdir -p ~/contador-data
 
docker run -d \
  --name contador \
  -p 5000:5000 \
  -v ./contador-data:/data \
  contador:v2
 
curl http://localhost:5000
curl http://localhost:5000
curl http://localhost:5000
 
# Mira el archivo DESDE EL HOST:
cat ./contador-data/contador.txt
```
 
Puedes ver el archivo desde el host. Ahora mata y revive el contenedor:
 
```bash
docker rm -f contador
docker run -d --name contador -p 5000:5000 -v ./contador-data:/data contador:v2
 
curl http://localhost:5000
```
 
**El contador continúa donde quedó.** Los datos sobrevivieron porque viven en el host.
 
### Paso 4 — Volumen nombrado: gestionado por Docker
 
Limpia y prueba con un volumen nombrado:
 
```bash
docker rm -f contador
docker volume create contador-data
docker volume ls
docker volume inspect contador-data
 
docker run -d \
  --name contador \
  -p 5000:5000 \
  -v contador-data:/data \
  contador:v2
 
curl http://localhost:5000
curl http://localhost:5000
```
 
El volumen vive en una ruta gestionada por Docker (en Linux: `/var/lib/docker/volumes/contador-data/_data`). No es tan accesible desde el host como un bind mount, pero es más portable y limpio.
 
Demuestra que sobrevive:
 
```bash
docker rm -f contador
docker run -d --name contador -p 5000:5000 -v contador-data:/data contador:v2
curl http://localhost:5000   # continúa
```
 
### Paso 5 — tmpfs: datos en RAM (no persisten)
 
```bash
docker rm -f contador
docker run -d \
  --name contador \
  -p 5000:5000 \
  --tmpfs /data \
  contador:v2
 
curl http://localhost:5000
curl http://localhost:5000
docker exec contador mount | grep data    # ve que es un tmpfs
docker rm -f contador
 
docker run -d --name contador -p 5000:5000 --tmpfs /data contador:v2
curl http://localhost:5000   # vuelve a 1
```
 
`tmpfs` guarda en RAM, no en disco. Útil para cachés temporales o datos sensibles que NO deben quedar en disco.
 
### Paso 6 — Limpia
 
```bash
docker rm -f contador
docker volume rm contador-data
rm -rf ./contador-data
```

---

---
 
## Lab 4 — Multi-contenedor con `docker run`: Flask + Redis (60 min)
 
**Mapea a:** Slides 15, 16, 20, 21 (contenedores y redes en acción)
 
**Objetivo:** Levantar la versión 3 de nuestra app, donde Flask y Redis viven en contenedores separados. Hacerlo TODO con comandos manuales para sentir el dolor antes del Compose.
 
### Paso 1 — Versión 3 de la app
 
Modifica `app.py`. Ahora el contador vive en Redis, un servicio aparte:
 
```python
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
    return f"Esta página ha sido visitada {n} veces.\n"
 
@app.route('/reset')
def reset():
    cache.set('visitas', 0)
    return "Contador reiniciado.\n"
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```
 
Añade `redis` al `requirements.txt`:
 
```
flask
redis
```
 
El `Dockerfile` no cambia. Reconstruye:
 
```bash
docker build -t contador:v3 .
```
 
### Paso 2 — Crea la red
 
Los dos contenedores deben verse por nombre, así que necesitamos una red bridge personalizada:
 
```bash
docker network create contador-net
```
 
### Paso 3 — Levanta Redis con persistencia
 
```bash
docker volume create redis-data
 
docker run -d \
  --name redis \
  --network contador-net \
  -v redis-data:/data \
  redis:7-alpine \
  redis-server --appendonly yes
```
 
- `--name redis` → así se llamará en el DNS interno de la red. La app Flask lo busca con ese nombre.
- `--network contador-net` → red personalizada (la default no resuelve nombres).
- `-v redis-data:/data` → volumen para que los datos sobrevivan.
- `--appendonly yes` → Redis hace fsync de cada escritura. Sin esto, en una caída perderías los últimos segundos.
Verifica que Redis está vivo:
 
```bash
docker exec redis redis-cli ping     # debe responder PONG
```
 
### Paso 4 — Levanta la app Flask
 
```bash
docker run -d \
  --name contador \
  --network contador-net \
  -p 5000:5000 \
  -e REDIS_HOST=redis \
  contador:v3
```
 
Nota que **NO publicamos el puerto de Redis**. Redis es interno: solo Flask lo necesita, y Flask vive en la misma red.
 
### Paso 5 — Pruébalo
 
```bash
curl http://localhost:5000
curl http://localhost:5000
curl http://localhost:5000
```
 
Cada hit incrementa el contador en Redis. Verifica directamente desde Redis:
 
```bash
docker exec redis redis-cli GET visitas
```
 
### Paso 6 — Demuestra que ahora SÍ es robusto
 
Mata SOLO la app Flask. Redis sigue corriendo. Vuelve a levantar Flask:
 
```bash
docker rm -f contador
 
docker run -d \
  --name contador \
  --network contador-net \
  -p 5000:5000 \
  -e REDIS_HOST=redis \
  contador:v3
 
curl http://localhost:5000   # continúa donde quedó
```
 
Ahora la prueba dura: mata TODO, incluyendo Redis, pero conserva el volumen:
 
```bash
docker rm -f contador redis
 
docker run -d --name redis --network contador-net -v redis-data:/data redis:7-alpine redis-server --appendonly yes
 
docker run -d --name contador --network contador-net -p 5000:5000 -e REDIS_HOST=redis contador:v3
 
curl http://localhost:5000   # SIGUE continuando
```
 
Los datos vivían en el volumen `redis-data`, no en el contenedor.
 
### Paso 7 — Reflexiona sobre lo tedioso que fue esto
 
Cuenta los comandos que tuviste que ejecutar para levantar la app: red, volumen, redis con sus banderas, app con sus banderas, variables de entorno, orden correcto... Para apagar todo:
 
```bash
docker rm -f contador redis
docker network rm contador-net
# El volumen se queda; si quieres tirarlo:
docker volume rm redis-data
```
 
**Imagina** que en lugar de 2 servicios fueran 6 (frontend, API, base de datos, caché, worker, broker). Imagina además que tienes que documentar todo esto para que otro compañero lo levante. Imagina que hay que versionarlo en Git.
 
Ese problema es el que Docker Compose resuelve.
 
### Preguntas de cierre
 
- ¿Qué pasaría si arrancaras el contenedor Flask ANTES que Redis? (Pruébalo: levanta solo Flask sin Redis y haz `curl`.) ¿Cómo se manifiesta el error?
- ¿Por qué no publicamos el puerto 6379 de Redis al host? ¿Qué riesgos de seguridad evitamos?
- Si quisieras que la app Flask aceptara también en HTTPS, ¿añadirías eso a la misma imagen o levantarías un contenedor aparte (ej. Caddy o Nginx)?
---
 
## Lab 7 — La misma app con Docker Compose (75 min)
 
**Mapea a:** Slides 24, 25, 26, 27, 28 (Docker Compose, servicios, archivos declarativos)
 
**Objetivo:** Replicar EXACTAMENTE el setup del Lab 6 con un archivo declarativo. Apreciar la diferencia. Después añadir features que con `docker run` serían dolorosas (escalar, healthchecks, dependencias).
 
### Paso 1 — Carpeta nueva
 
```bash
mkdir lab4-compose && cd lab4-compose
```
 
Copia `app.py`, `requirements.txt` y `Dockerfile` del Lab 6 a esta carpeta nueva.
 
### Paso 2 — Crea `docker-compose.yml`
 
Este archivo reemplaza TODO el laberinto de comandos del Lab 6:
 
```yaml
services:
  contador:
    build: .
    container_name: contador_app
    ports:
      - "5000:5000"
    environment:
      REDIS_HOST: redis
    depends_on:
      - redis
    restart: unless-stopped
 
  redis:
    image: redis:7-alpine
    container_name: contador_redis
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    restart: unless-stopped
 
volumes:
  redis-data:
```
 
Observa lo que YA NO tienes que hacer:
- No declaras la red — Compose crea una automáticamente para los servicios del proyecto.
- No declaras las dependencias de nombres DNS — los servicios se resuelven por su nombre de servicio.
- No tienes que ejecutar 6 comandos en el orden correcto.
### Paso 3 — Levanta todo
 
```bash
docker compose up -d --build
docker compose ps
docker compose logs -f
```
 
(Ctrl+C para salir de `logs -f`; no detiene los contenedores).
 
### Paso 4 — Pruébalo
 
```bash
curl http://localhost:5000
curl http://localhost:5000
curl http://localhost:5000
```
 
Funciona idéntico al Lab 6, pero con UN comando para todo.
 
### Paso 5 — Persistencia entre apagados
 
```bash
docker compose down              # tira contenedores y red, conserva el volumen
curl http://localhost:5000       # esto FALLA: nada está corriendo
docker compose up -d
curl http://localhost:5000       # continúa donde quedó
```
 
### Paso 6 — Modificación en vivo
 
Cambia el mensaje en `app.py`. Reconstruye solo la imagen afectada:
 
```bash
docker compose up -d --build
curl http://localhost:5000
```
 
Compose detecta el cambio, reconstruye, y reemplaza el contenedor sin tocar Redis.
