FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código del bot
COPY bot/ .

# Crear directorio para logs
RUN mkdir -p /app/logs

# Comando para ejecutar el bot
CMD ["python", "main.py"]