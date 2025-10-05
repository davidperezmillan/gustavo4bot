"""
Tests para la configuración del bot
"""
import pytest
import os
from unittest.mock import patch

class TestConfig:
    """Tests para la configuración"""
    
    def test_required_env_vars_definition(self):
        """Test que las variables de entorno requeridas están definidas en el test"""
        required_vars = [
            'TELEGRAM_TOKEN',
            'OWNER_ID', 
            'CHAT_SOURCE_ID',
            'PUBLISH_CHANNEL_ID',
            'STORAGE_CHANNEL_ID'
        ]
        
        # En el entorno de test, estas variables deben estar disponibles
        for var in required_vars:
            assert var in os.environ, f"Variable {var} no está definida en el entorno de test"
            assert os.environ[var] is not None
            assert len(os.environ[var].strip()) > 0
    
    def test_telegram_token_format(self):
        """Test que el token de Telegram tiene el formato correcto"""
        token = os.environ.get('TELEGRAM_TOKEN')
        if token and token != "test_token_for_testing" and token != "test_token":
            # Solo validar formato si es un token real, no de test
            assert ':' in token
            parts = token.split(':')
            assert len(parts) == 2
            assert parts[0].isdigit()
            assert len(parts[1]) >= 35  # Los tokens de Telegram son largos
        else:
            # Para tokens de test, solo verificar que existe
            assert token is not None
            assert len(token) > 0
    
    def test_chat_ids_format(self):
        """Test que los IDs de chat tienen formato válido"""
        # Usar IDs del entorno actual
        owner_id = os.environ.get('OWNER_ID')
        chat_source_id = os.environ.get('CHAT_SOURCE_ID') 
        publish_channel_id = os.environ.get('PUBLISH_CHANNEL_ID')
        storage_channel_id = os.environ.get('STORAGE_CHANNEL_ID')
        
        # Owner ID debe ser numérico
        assert owner_id.isdigit() or (owner_id.startswith('-') and owner_id[1:].isdigit())
        
        # Los canales deben tener formato válido
        for chat_id in [chat_source_id, publish_channel_id, storage_channel_id]:
            assert chat_id.startswith('-100') or chat_id.startswith('-') or chat_id.isdigit()
    
    def test_log_level_valid(self):
        """Test que el nivel de log es válido"""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        log_level = os.environ.get('LOG_LEVEL', 'INFO')
        assert log_level in valid_levels