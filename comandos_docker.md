# Comandos más utilizados en Docker

## Información del sistema
- `docker --version`
- `docker info`
- `docker system df`

## Imágenes
- `docker pull <imagen>`
- `docker images`
- `docker rmi <imagen>`
- `docker build -t <nombre> .`

## Contenedores
- `docker ps`
- `docker ps -a`
- `docker run <imagen>`
- `docker run -d <imagen>`
- `docker run -p <host:container> <imagen>`
- `docker start <contenedor>`
- `docker stop <contenedor>`
- `docker restart <contenedor>`
- `docker rm <contenedor>`

## Logs y monitoreo
- `docker logs <contenedor>`
- `docker logs -f <contenedor>`
- `docker top <contenedor>`
- `docker stats`

## Exec
- `docker exec -it <contenedor> /bin/bash`
- `docker exec -it <contenedor> <comando>`

## Redes
- `docker network ls`
- `docker network create <nombre>`
- `docker network inspect <nombre>`

## Volúmenes
- `docker volume ls`
- `docker volume create <nombre>`
- `docker volume inspect <nombre>`

## Docker Compose
- `docker compose up`
- `docker compose up -d`
- `docker compose down`
- `docker compose ps`
- `docker compose logs -f`

