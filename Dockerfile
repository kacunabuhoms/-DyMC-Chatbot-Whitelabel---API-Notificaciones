# 1. Imagen base de Python
FROM python:3.11-slim

# 2. Configuración para que los logs se vean bien en Google Cloud
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

WORKDIR /app

# 3. Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar el código
COPY . .

# 5. Ejecutar con Uvicorn
# Importante: usamos src.interfaces.main:app porque así está en tu estructura
CMD ["uvicorn", "src.interfaces.main:app", "--host", "0.0.0.0", "--port", "8080"]