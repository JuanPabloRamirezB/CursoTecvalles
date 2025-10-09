# 2.- Bind Mounts (montaje directo de una carpeta del host)

## Definición: 
Montan un directorio o archivo del sistema host directamente en un contenedor.

## Uso típico:
Utilizados en desarrollo cuando quieres que los cambios locales (en tu sistema) se reflejen de inmediato dentro del contenedor.

## Idea:
static-server — sirve archivos estáticos desde /site con http.server. Al editar los archivos en tu host, los cambios se ven al instante.

### Estructura
```
Practica1/
    └─ Prueba2/
        ├─ Dockerfile
        └─ site/
            └─ index.html

```

### Construir
```
docker build -t imagen-practica-prueba2 .

```

### Ejecutar
```
docker run --rm --name web1 -d \
  -p 8080:8000 \
  -v "$(pwd)/site":/site imagen-practica-prueba2
```