# 2.- Bind Mounts (montaje directo de una carpeta del host)

## Definición: 
Montan un directorio o archivo del sistema host directamente en un contenedor.

## Uso típico:
Utilizados en desarrollo cuando quieres que los cambios locales (en tu sistema) se reflejen de inmediato dentro del contenedor.

## Idea:
La app agrega una nota a un archivo persistente en "$(pwd)"/host_data/notas.txt y luego imprime su contenido.

### Estructura
```
Practica1/
    └─ Prueba1
        ├─ Dockerfile
        └─ app.py
```

### Construir
```
docker build -t imagen-practica1 .
mkdir -p ./host_data
```

### Ejecutar
```
docker run --rm -e MENSAJE="Hola desde Volume2" -v "$(pwd)"/host_data:/data imagen-practica1
```