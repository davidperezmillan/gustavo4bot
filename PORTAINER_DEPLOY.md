# Instrucciones para desplegar gustavo4bot en Portainer

## Método 1: Build desde GitHub (Recomendado)

1. **Subir código a GitHub** (si no está ya):
   ```bash
   git add .
   git commit -m "Add gustavo4bot"
   git push origin main
   ```

2. **En Portainer**:
   - Ve a "Stacks"
   - Click "Add stack"
   - Nombre: `gustavo4bot`
   - Method: "Repository"
   - Repository URL: `https://github.com/davidperezmillan/CdO`
   - Repository reference: `refs/heads/main`
   - Compose path: `bots/gustavo4bot/portainer-stack-build.yml`
   
3. **Configurar variables de entorno**:
   ```
   TELEGRAM_TOKEN=7850932225:AAF5ACUWuvwI0Av8tt9Q4_yRXBWPFlxbxa0
   OWNER_ID=14824267
   CHAT_SOURCE_ID=-1001234567890
   PUBLISH_CHANNEL_ID=-1002795030702
   STORAGE_CHANNEL_ID=-1002834323493
   LOG_LEVEL=INFO
   TZ=Europe/Madrid
   ```

4. **Deploy** el stack

## Método 2: Docker Hub Registry

1. **Construir y subir imagen**:
   ```bash
   docker build -t davidperezmillan/gustavo4bot:latest .
   docker push davidperezmillan/gustavo4bot:latest
   ```

2. **Usar portainer-stack.yml** cambiando la imagen a:
   ```yaml
   image: davidperezmillan/gustavo4bot:latest
   ```

## Método 3: Build local y copiar

1. **Guardar imagen**:
   ```bash
   docker save gustavo4bot:latest > gustavo4bot.tar
   ```

2. **Cargar en nodo de Portainer**:
   ```bash
   docker load < gustavo4bot.tar
   ```

3. **Usar portainer-stack.yml** original

## Variables de entorno requeridas

Las siguientes variables deben configurarse en Portainer:

- `TELEGRAM_TOKEN`: Token del bot
- `OWNER_ID`: ID del propietario del bot
- `CHAT_SOURCE_ID`: ID del chat fuente
- `PUBLISH_CHANNEL_ID`: ID del canal de publicación  
- `STORAGE_CHANNEL_ID`: ID del canal de almacenamiento
- `LOG_LEVEL`: Nivel de logs (INFO por defecto)
- `TZ`: Zona horaria (Europe/Madrid por defecto)