# INSTRUCCIONES PARA PORTAINER

## 📋 Pasos para desplegar Gustavo4Bot en Portainer

### 1. Construir la imagen localmente
```bash
cd /home/david/docker/bots/gustavo4bot
./build.sh
```

### 2. En Portainer Web UI:
1. Ir a **Stacks** > **Add Stack**
2. **Name**: `gustavo4bot`
3. **Build method**: `Web editor`
4. Copiar el contenido del archivo `portainer-stack.yml`

### 3. Variables de entorno a configurar:

```
TELEGRAM_TOKEN=7850932225:AAF5ACUWuvwI0Av8tt9Q4_yRXBWPFlxbxa0
OWNER_ID=
CHAT_SOURCE_ID=
PUBLISH_CHANNEL_ID=
STORAGE_CHANNEL_ID=
LOG_LEVEL=INFO
TZ=Europe/Madrid
```

### 4. Obtener los IDs necesarios:

**Tu ID de usuario:**
- Envía `/start` a @userinfobot en Telegram
- El bot te responderá con tu ID (ej: 123456789)

**IDs de chats/canales:**
- Agrega @userinfobot al chat o canal
- El bot mostrará el ID (ej: -1001234567890)
- Los IDs de grupos/canales siempre empiezan con -100

### 5. Configurar permisos del bot:

El bot debe ser **administrador** en:
- ✅ Chat fuente (para leer mensajes)
- ✅ Canal de publicación (para enviar con spoiler)
- ✅ Canal de almacenamiento (para guardar archivos)

### 6. Deploy y monitoreo:

1. Click **Deploy the stack**
2. Ir a **Containers** para ver el estado
3. Ver logs en **Containers** > `gustavo4_bot` > **Logs**

### 7. Verificar funcionamiento:

1. Enviar una imagen al chat fuente configurado
2. Deberías recibir un mensaje con botones en tu chat privado
3. Probar cada opción: Enviar, Enviar con leyenda, Almacenar, Descartar

---

## 🔧 Troubleshooting

**Si el bot no responde:**
- Verificar que los IDs estén correctos
- Verificar permisos de administrador
- Revisar logs del contenedor

**Si no puede enviar a canales:**
- Verificar que el bot sea admin de los canales
- Verificar que los IDs de canales sean correctos (-100...)

**Para actualizar:**
1. Rebuild imagen: `./build.sh`
2. En Portainer: **Stacks** > `gustavo4bot` > **Update the stack**