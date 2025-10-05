# GitHub Actions + Portainer Deployment

Este repositorio está configurado para hacer despliegue automático a Portainer usando webhooks, **con testing automático incluido**.

## 🧪 Testing Automático

### Tests incluidos en CI/CD
- ✅ **Tests unitarios** de todas las funcionalidades
- ✅ **Tests de integración** del flujo completo
- ✅ **Linting** con flake8, black, isort
- ✅ **Type checking** con mypy
- ✅ **Coverage reporting** con pytest-cov

### Workflows de testing
1. **`tests.yml`** - Tests completos en múltiples versiones de Python
2. **`deploy-portainer.yml`** - Tests + deployment simple
3. **`deploy-advanced.yml`** - Tests + deployment avanzado con reintentos

## 🚀 Cómo funciona

### Pipeline completo
```
Código → Tests → ✅/❌ → Deploy (solo si tests pasan)
```

### Trigger automático
- ✅ **Pull Requests**: Solo ejecuta tests (no despliega)
- ✅ **Push a main/master**: Tests + deployment automático
- ✅ **Ejecución manual**: Con opciones para saltar tests

### Webhooks de Portainer
- 🔗 URL: `http://portainer.davidperezmillan.com/api/stacks/webhooks/1e5f595f-f205-4ae0-b2ff-ff007a535e80`
- 📦 Stack ID configurado en Portainer
- 🔄 Actualización automática del stack
- 🛡️ **Solo se despliega si todos los tests pasan**

## 📋 Workflows disponibles

### 1. **tests.yml** (Solo Testing)
- Tests en múltiples versiones de Python (3.9, 3.10, 3.11)
- Linting completo y type checking
- Se ejecuta en PRs y daily
- Ideal para desarrollo

### 2. **deploy-portainer.yml** (Simple con Tests)
- Tests + deployment básico con webhook
- Perfecto para casos simples
- Falla si los tests no pasan

### 3. **deploy-advanced.yml** (Avanzado con Tests)
- Tests + reintentos automáticos (3 intentos)
- Mejor manejo de errores
- Información detallada del deployment
- Resumen en GitHub Actions
- Deployment manual opcional
- Opción para saltar tests (no recomendado)

## 🧪 Testing Local

### Ejecutar tests localmente:
```bash
# Instalar dependencias de test
pip install -r requirements-test.txt

# Método 1: Script automatizado
./run-tests.sh                    # Tests básicos
./run-tests.sh -c                 # Con coverage
./run-tests.sh -i -v              # Instalar deps + verbose
./run-tests.sh --lint-only        # Solo linting

# Método 2: Pytest directo  
pytest                            # Tests básicos
pytest --cov=bot --cov-report=html  # Con coverage HTML
pytest -v                         # Verbose
pytest tests/test_config.py       # Tests específicos
```

### Estructura de tests:
```
tests/
├── conftest.py              # Configuración pytest + fixtures
├── test_config.py           # Tests de configuración
├── test_integration.py      # Tests de integración
├── test_handlers/           # Tests de handlers
│   ├── test_command_handler.py
│   ├── test_message_handler.py
│   └── test_callback_handler.py
└── test_utils/              # Tests de utilidades
    └── test_media_utils.py
```

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