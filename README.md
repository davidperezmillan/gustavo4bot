# 🤖 Gustavo4Bot

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)](https://www.docker.com/)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://core.telegram.org/bots)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Bot de Telegram para **gestión automatizada de multimedia** con funcionalidades avanzadas de procesamiento y distribución.

## ✨ Características Principales

- 🔍 **Detección automática** de multimedia (imágenes, videos, animaciones)
- 📤 **Reenvío inteligente** al propietario con botones de acción
- 🏷️ **Gestión con botones interactivos**:
  - 📨 **Enviar con spoiler** al canal de publicación
  - ✍️ **Enviar con leyenda personalizada** + spoiler
  - 🗄️ **Almacenar** en canal de archivos
  - 🗑️ **Descartar** sin procesar
- 🧹 **Eliminación automática** del mensaje original después del procesamiento
- 🔄 **Sistema de colas** para manejo concurrente de multimedia
- 📊 **Logs detallados** para monitoreo y debugging

## 🚀 Instalación Rápida

### 🐳 Con Docker (Recomendado)

```bash
# Clonar repositorio
git clone https://github.com/davidperezmillan/gustavo4bot.git
cd gustavo4bot

# Configurar variables de entorno
cp .env.example .env
nano .env  # Editar con tus valores

# Ejecutar con Docker Compose
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f
```

### 🐍 Instalación Manual

```bash
# Clonar e instalar dependencias
git clone https://github.com/davidperezmillan/gustavo4bot.git
cd gustavo4bot
pip install -r requirements.txt

# Configurar variables de entorno
export TELEGRAM_TOKEN="tu_token_aqui"
export OWNER_ID="tu_user_id"
# ... otras variables

# Ejecutar
cd bot
python main.py
```

## ⚙️ Configuración

### 1. Variables de Entorno

Crea un archivo `.env` con la siguiente configuración:

```bash
# Token del bot de Telegram
TELEGRAM_TOKEN=tu_token_del_bot

# IDs de configuración - PERSONALIZAR
OWNER_ID=tu_user_id
CHAT_SOURCE_ID=id_del_chat_fuente
PUBLISH_CHANNEL_ID=id_canal_publicacion
STORAGE_CHANNEL_ID=id_canal_almacenamiento

# Configuración adicional
LOG_LEVEL=INFO
TZ=Europe/Madrid
```

### 2. Obtener IDs Necesarios

| ID Requerido | Cómo Obtenerlo |
|--------------|----------------|
| **OWNER_ID** | Envía `/start` a [@userinfobot](https://t.me/userinfobot) |
| **CHAT_SOURCE_ID** | Agrega [@userinfobot](https://t.me/userinfobot) al chat/grupo |
| **PUBLISH_CHANNEL_ID** | Agrega [@userinfobot](https://t.me/userinfobot) al canal |
| **STORAGE_CHANNEL_ID** | Agrega [@userinfobot](https://t.me/userinfobot) al canal |

> **💡 Nota:** Los IDs de canales/grupos empiezan con `-100`

### 3. Permisos del Bot

El bot necesita ser **administrador** con los siguientes permisos:

- **Chat fuente**: `Delete messages`, `Read messages`
- **Canal de publicación**: `Post messages`, `Edit messages`
- **Canal de almacenamiento**: `Post messages`, `Edit messages`

## 🏗️ Arquitectura del Proyecto

```
gustavo4bot/
├── 🤖 bot/
│   ├── main.py                 # 🚀 Punto de entrada principal
│   ├── config.py               # ⚙️ Configuración y constantes
│   ├── keyboards.py            # 🎹 Botones inline interactivos
│   ├── 🎛️ handlers/
│   │   ├── __init__.py
│   │   ├── message_handler.py  # 📥 Procesamiento de multimedia
│   │   ├── callback_handler.py # 🔘 Manejo de botones
│   │   ├── command_handler.py  # 💬 Comandos del bot
│   │   └── conversation_handler.py # 🗣️ Conversaciones
│   └── 🛠️ utils/
│       ├── __init__.py
│       └── media_utils.py      # 🖼️ Utilidades multimedia
├── 🐳 Docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── build.sh
├── 📋 Portainer/
│   ├── portainer-stack.yml
│   └── PORTAINER_DEPLOY.md
├── requirements.txt
├── .env.example
└── README.md
```

## 🔄 Flujo de Trabajo

1. **🔍 Detección**: Bot detecta multimedia en chat fuente
2. **📤 Reenvío**: Envía al propietario con botones de acción
3. **👆 Selección**: Propietario elige acción:
   - **📨 Enviar**: Publica con spoiler en canal
   - **✍️ Enviar con leyenda**: Solicita texto y publica con spoiler
   - **🗄️ Almacenar**: Guarda en canal de archivos
   - **🗑️ Descartar**: Elimina sin procesar
4. **🧹 Limpieza**: Elimina mensaje original automáticamente

## 🚀 Despliegue con Portainer

### 1. Preparar Imagen

```bash
# Ejecutar script de construcción
./build.sh

# O manualmente
docker build -t gustavo4bot:latest .
```

### 2. Stack en Portainer

1. **Portainer** → **Stacks** → **Add Stack**
2. **Nombre**: `gustavo4bot`
3. **Web editor**: Copiar contenido de `portainer-stack.yml`
4. **Environment variables**:
   ```
   TELEGRAM_TOKEN=tu_token
   OWNER_ID=tu_id
   CHAT_SOURCE_ID=id_chat_fuente
   PUBLISH_CHANNEL_ID=id_canal_publicacion
   STORAGE_CHANNEL_ID=id_canal_almacenamiento
   ```
5. **Deploy**

## 📊 Monitoreo y Logs

### Ver Logs en Tiempo Real

```bash
# Con Docker Compose
docker-compose logs -f gustavo4bot

# Con Docker directo
docker logs -f gustavo4_bot

# Logs específicos
docker-compose logs --tail=50 gustavo4bot
```

### Estructura de Logs

Los logs incluyen información detallada sobre:
- 🚀 Inicio del bot y configuración
- 📥 Recepción de multimedia
- 📤 Reenvío al propietario
- 🔘 Interacciones con botones
- 📨 Envíos a canales
- 🧹 Eliminaciones automáticas
- ❌ Errores y advertencias

## 🛠️ Comandos Útiles

```bash
# 🔄 Gestión del contenedor
docker-compose up -d          # Iniciar en background
docker-compose down           # Parar y eliminar
docker-compose restart        # Reiniciar
docker-compose up --build -d  # Reconstruir e iniciar

# 📊 Monitoreo
docker-compose ps             # Estado de contenedores
docker-compose logs -f        # Logs en tiempo real
docker-compose exec gustavo4bot bash  # Acceso al contenedor

# 🧹 Limpieza
docker system prune -f        # Limpiar recursos Docker
docker-compose down -v        # Parar y eliminar volúmenes
```

## 🔧 Desarrollo

### Estructura de Handlers

- **`message_handler.py`**: Procesa multimedia entrante
- **`callback_handler.py`**: Maneja clicks en botones
- **`command_handler.py`**: Comandos como `/start`, `/help`
- **`conversation_handler.py`**: Flujos de conversación para leyendas

### Sistema de Colas

El bot implementa un sistema basado en `message_id` para:
- ✅ Evitar conflictos con multimedia concurrente
- ✅ Asociar botones con su multimedia específica
- ✅ Limpiar datos después del procesamiento

## 🤝 Contribución

1. **Fork** el proyecto
2. **Crea** una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Abre** un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 📞 Soporte

- 🐛 **Issues**: [GitHub Issues](https://github.com/davidperezmillan/gustavo4bot/issues)
- 📧 **Email**: david.perez.millan@example.com
- 💬 **Telegram**: [@davidperezmillan](https://t.me/davidperezmillan)

---

<div align="center">

**🤖 Desarrollado con ❤️ por [davidperezmillan](https://github.com/davidperezmillan)**

⭐ **¡Dale una estrella si te ha sido útil!** ⭐

</div>