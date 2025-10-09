# 3.- tmpfs Mount (en RAM, datos efímeros)

## Definición: 
Se montan directamente en memoria RAM del host (sin escribir en disco).

## Uso típico:
Ideal para datos temporales o sensibles que no deben persistir, como credenciales, archivos de sesión, o cachés.

## Idea:
La app crea archivos temporales en /cache (montada en RAM) y muestra su contenido.

### Estructura
```
Practica3/
├─ Dockerfile
└─ app.py
```

### Construir
```
docker build -t practica3-tmpfs-cache .

```

### Ejecutar
```
docker run --rm --tmpfs /cache:rw,size=64m practica3-tmpfs-cache
```