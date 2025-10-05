# Tests para Gustavo4Bot

Este directorio contiene todas las pruebas automatizadas del bot.

## Estructura

```
tests/
├── __init__.py
├── conftest.py              # Configuración de pytest
├── test_config.py           # Tests de configuración
├── test_handlers/           # Tests de handlers
│   ├── __init__.py
│   ├── test_command_handler.py
│   ├── test_message_handler.py
│   └── test_callback_handler.py
├── test_utils/              # Tests de utilidades
│   ├── __init__.py
│   └── test_media_utils.py
└── mocks/                   # Mocks y fixtures
    ├── __init__.py
    └── telegram_mocks.py
```

## Ejecutar tests

```bash
# Instalar dependencias de test
pip install -r requirements-test.txt

# Ejecutar todos los tests
pytest

# Ejecutar con coverage
pytest --cov=bot --cov-report=html

# Ejecutar tests específicos
pytest tests/test_config.py
```

## Tipos de tests

- **Unit tests**: Funciones individuales
- **Integration tests**: Interacción entre componentes
- **Mock tests**: Simulación de Telegram API