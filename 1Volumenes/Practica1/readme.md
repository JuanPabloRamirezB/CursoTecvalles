# 1.- Volúmenes (Volumes)

## Definición: 
Son los más comunes y recomendados por Docker. Se crean y gestionan directamente por Docker en su directorio interno (normalmente /var/lib/docker/volumes/).

## Uso típico:
Ideal para datos persistentes que deben mantenerse aunque se elimine el contenedor (por ejemplo, bases de datos, archivos de configuración o logs).

## Idea:
La app agrega una nota a un archivo persistente en /data/notas.txt y luego imprime su contenido.

### Estructura
```
Practica1/
    ├─ Dockerfile
    └─ app.py
```
### Comandos basicos
```
docker volume create my-vol

docker volume ls

docker volume inspect my-vol

docker volume rm my-vol
```

### Construir
```
docker build -t imagen-practica1 .
docker volume create volumen-practica1
```

### Ejecutar
```
docker run --rm -e MENSAJE="Hola desde Volume" -v volumen-practica1:/data imagen-practica1
```