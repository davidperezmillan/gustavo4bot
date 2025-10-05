# Gustavo4Bot

Bot de Telegram para gestión automatizada de multimedia.

## Funcionalidades

- **Recuperación automática**: Detecta imágenes, videos y animaciones de un chat específico
- **Reenvío al propietario**: Envía el contenido al propietario con botones de acción
- **Gestión con botones**:
  - **Enviar**: Envía al canal con spoiler
  - **Enviar con leyenda**: Permite agregar texto personalizado con spoiler
  - **Almacenar**: Guarda en canal de archivos
  - **Descartar**: Elimina sin procesar

## Configuración

### 1. Variables de entorno (.env)

El bot usa variables de entorno para la configuración. Edita el archivo `.env`:

```bash
# Token del bot de Telegram
TELEGRAM_TOKEN=7850932225:AAF5ACUWuvwI0Av8tt9Q4_yRXBWPFlxbxa0

# IDs de configuración - CAMBIAR ESTOS VALORES
OWNER_ID=123456789
CHAT_SOURCE_ID=-1001234567890
PUBLISH_CHANNEL_ID=-1001234567891
STORAGE_CHANNEL_ID=-1001234567892

# Configuración adicional
LOG_LEVEL=INFO
TZ=Europe/Madrid
```

### 2. Cómo obtener los IDs

**Tu ID de usuario:**
- Envía `/start` a [@userinfobot](https://t.me/userinfobot)

**ID de canales/grupos:**
- Agrega [@userinfobot](https://t.me/userinfobot) al canal/grupo
- Los IDs de canales/grupos empiezan con `-100`

### 3. Configurar permisos

**Bot debe ser:**
- Administrador en el chat fuente (para leer mensajes)
- Administrador en canales de publicación y almacenamiento (para enviar)

## Instalación

### 🐳 Con Portainer (Recomendado)

#### 1. Construir la imagen

```bash
cd /home/david/docker/bots/gustavo4bot
./build.sh
```

#### 2. Desplegar en Portainer

1. **Ir a Portainer** > Stacks > Add Stack
2. **Nombre del stack**: `gustavo4bot`
3. **Copiar contenido** de `portainer-stack.yml`
4. **Configurar variables de entorno**:
   ```
   TELEGRAM_TOKEN=7850932225:AAF5ACUWuvwI0Av8tt9Q4_yRXBWPFlxbxa0
   OWNER_ID=[TU_ID_DE_USUARIO]
   CHAT_SOURCE_ID=[ID_DEL_CHAT_FUENTE]
   PUBLISH_CHANNEL_ID=[ID_DEL_CANAL_PUBLICACION]
   STORAGE_CHANNEL_ID=[ID_DEL_CANAL_ALMACENAMIENTO]
   LOG_LEVEL=INFO
   TZ=Europe/Madrid
   ```
5. **Deploy the stack**

### 🐳 Con Docker Compose

```bash
# Navegar al directorio
cd /home/david/docker/bots/gustavo4bot

# Configurar variables en .env
nano .env

# Ejecutar
docker-compose up -d

# Ver logs
docker-compose logs -f
```

### 🐍 Manual

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
export TELEGRAM_TOKEN="7850932225:AAF5ACUWuvwI0Av8tt9Q4_yRXBWPFlxbxa0"
export OWNER_ID="123456789"
# ... otras variables

# Ejecutar
cd bot
python main.py
```

## Estructura del proyecto

```
gustavo4bot/
├── bot/
│   ├── main.py                 # Punto de entrada
│   ├── config.py               # Configuración
│   ├── keyboards.py            # Botones inline
│   ├── handlers/
│   │   ├── message_handler.py  # Manejo de multimedia
│   │   ├── callback_handler.py # Manejo de botones
│   │   └── conversation_handler.py # Conversaciones
│   └── utils/
│       └── media_utils.py      # Utilidades multimedia
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Flujo de trabajo

1. **Detección**: El bot detecta multimedia en el chat fuente
2. **Reenvío**: Envía al propietario con botones de acción
3. **Selección**: El propietario elige una acción:
   - **Enviar**: Publica con spoiler en el canal
   - **Enviar con leyenda**: Solicita texto y publica con spoiler
   - **Almacenar**: Guarda en canal de archivos
   - **Descartar**: Elimina sin procesar

## Logs

Los logs se guardan en:
- Docker: `./logs/bot.log`
- Manual: `/app/logs/bot.log`

## Comandos útiles

```bash
# Ver logs en tiempo real
docker-compose logs -f gustavo4bot

# Reiniciar bot
docker-compose restart gustavo4bot

# Parar bot
docker-compose down

# Actualizar y reiniciar
docker-compose up -d --build
```

## Token del bot

El token está configurado directamente en `config.py`:
```
7850932225:AAF5ACUWuvwI0Av8tt9Q4_yRXBWPFlxbxa0
```

Para mayor seguridad, considera usar variables de entorno en producción.