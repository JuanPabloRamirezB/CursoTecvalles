# 2.- Host

## Definición: 
El contenedor comparte directamente la red del host, sin aislamiento de red.

## Uso típico:
Aplicaciones que necesitan rendimiento de red máximo o acceso directo (como monitoreo o servidores locales).

## Idea:
Crear un monitor ligero que mida la velocidad de la red del host (en tiempo real) y exponga un endpoint http://localhost:9999/net

### Estructura
```
Practica5/
    ├─ Dockerfile
    └─ app.py
```

### Construir
```
docker build -t imagen_practica5 .
```
### Ejecutar con trampa
```
docker run --rm -d --name practica5 -p 9999:9999 -e ENABLE_FLOOD=1 imagen_practica5
```

### Ejecutar
```
docker run --rm -d --network host --name practica5 -e ENABLE_FLOOD=1 imagen_practica5
```

### Comprobacion
```
curl http://localhost:9999/
curl http://localhost:9999/net
```

