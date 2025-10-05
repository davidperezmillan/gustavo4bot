# GitHub Actions + Portainer Deployment

Este repositorio está configurado para hacer despliegue automático a Portainer usando webhooks.

## 🚀 Cómo funciona

### Trigger automático
- ✅ Cada push a `main` o `master` dispara el deployment
- ✅ También se puede ejecutar manualmente desde GitHub Actions

### Webhooks de Portainer
- 🔗 URL: `http://portainer.davidperezmillan.com/api/stacks/webhooks/1e5f595f-f205-4ae0-b2ff-ff007a535e80`
- 📦 Stack ID configurado en Portainer
- 🔄 Actualización automática del stack

## 📋 Workflows disponibles

### 1. **deploy-portainer.yml** (Simple)
- Deployment básico con webhook
- Perfecto para casos simples
- Menos verbose

### 2. **deploy-advanced.yml** (Avanzado)
- Reintentos automáticos (3 intentos)
- Mejor manejo de errores
- Información detallada del deployment
- Resumen en GitHub Actions
- Deployment manual opcional

## 🎯 Proceso de deployment

1. **Push/Merge** → Trigger automático
2. **GitHub Actions** → Ejecuta el workflow
3. **Webhook Call** → Llama al endpoint de Portainer
4. **Portainer** → Actualiza el stack automáticamente
5. **Verification** → Verifica el estado del deployment

## 🔧 Configuración actual

```yaml
# Stack configurado en Portainer
Stack Name: gustavo4bot
Webhook ID: 1e5f595f-f205-4ae0-b2ff-ff007a535e80
Portainer URL: http://portainer.davidperezmillan.com
```

## 📖 Uso

### Deployment automático
```bash
# Hacer cambios en el código
git add .
git commit -m "Update bot functionality"
git push origin main  # ← Esto dispara el deployment automático
```

### Deployment manual
1. Ve a GitHub Actions en el repositorio
2. Selecciona "Advanced Deploy to Portainer"
3. Click en "Run workflow"
4. Opcionalmente marca "Force deployment"

## 🔍 Monitoreo

### En GitHub
- Ve a la pestaña **Actions** para ver el estado de los deployments
- Cada workflow muestra logs detallados
- El workflow avanzado incluye un resumen

### En Portainer
- Ve al [dashboard de Portainer](http://portainer.davidperezmillan.com)
- Revisa el estado del stack `gustavo4bot`
- Monitorea los logs del contenedor

## 🛠️ Troubleshooting

### Si el deployment falla:
1. **Revisa los logs** en GitHub Actions
2. **Verifica el webhook** en Portainer
3. **Comprueba la conectividad** a Portainer
4. **Ejecuta manualmente** el workflow avanzado

### Errores comunes:
- **HTTP 404**: Webhook no encontrado o eliminado
- **HTTP 500**: Error interno de Portainer
- **Timeout**: Problemas de red o Portainer sobrecargado

## 🔄 Actualizaciones del webhook

Si necesitas cambiar el webhook:
1. Ve a Portainer → Stacks → gustavo4bot
2. Copia el nuevo webhook URL
3. Actualiza el archivo `.github/workflows/deploy-*.yml`
4. Cambia la variable `PORTAINER_WEBHOOK_URL`

## 📝 Logs y debugging

Para ver logs detallados:
```bash
# En el servidor donde está Portainer
docker logs <container_id>

# O desde Portainer UI
# Stack → gustavo4bot → Containers → View logs
```