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
