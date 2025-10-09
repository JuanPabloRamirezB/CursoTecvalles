# 1.- Bridge (puente por defecto)

## Definición: 
Es la red predeterminada que Docker crea al instalarse. Si no especificas una red, tus contenedores se conectan aquí.

## Uso típico:
Aplicaciones simples que necesitan comunicación básica dentro del mismo host.

## Idea:
App que ingresa o lista articulos en una base de datos utilizando Bridge para comunicarse.

### Estructura
```
Practica4/
    └─ app/
        ├─ Dockerfile
        └─ app.py
```

### Construir
```
docker network create red_practica4

docker build -t imagen_practica4 ./app

```

### Ejecutar
```
docker run -d --name postgres --network red_practica4 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=secret -e POSTGRES_DB=tienda -v pg_data:/var/lib/postgresql/data postgres:16

docker run -d --name app --network red_practica4 -p 8080:8000   -e DB_USER=postgres -e DB_PASSWORD=secret -e DB_NAME=tienda -e DB_HOST=postgres   imagen_practica4
```
### Ejemplos de uso
```
curl http://localhost:8080/

curl -X POST http://localhost:8080/anadirproductos \
  -H "Content-Type: application/json" \
  -d '{"nombre":"teclado","precio":199.9}'

curl http://localhost:8080/listarproductos
```

### Ejecutar con Docker Compose
```
docker compose up -d
```