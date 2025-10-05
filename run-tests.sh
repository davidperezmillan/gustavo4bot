#!/bin/bash

# Script para ejecutar tests localmente
# Uso: ./run-tests.sh [options]

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar ayuda
show_help() {
    echo "🧪 Script de Tests para Gustavo4Bot"
    echo ""
    echo "Uso: $0 [opciones]"
    echo ""
    echo "Opciones:"
    echo "  -h, --help     Mostrar esta ayuda"
    echo "  -f, --fast     Ejecutar solo tests rápidos"
    echo "  -c, --coverage Ejecutar con reporte de coverage"
    echo "  -v, --verbose  Output detallado"
    echo "  -i, --install  Instalar dependencias antes de ejecutar"
    echo "  --lint-only    Solo ejecutar linting"
    echo "  --clean        Limpiar archivos de coverage anteriores"
    echo ""
    echo "Ejemplos:"
    echo "  $0 -c          # Tests con coverage"
    echo "  $0 -i -v       # Instalar deps y ejecutar con detalle"
    echo "  $0 --lint-only # Solo linting"
}

# Variables por defecto
FAST=false
COVERAGE=false
VERBOSE=false
INSTALL=false
LINT_ONLY=false
CLEAN=false

# Parsear argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -f|--fast)
            FAST=true
            shift
            ;;
        -c|--coverage)
            COVERAGE=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -i|--install)
            INSTALL=true
            shift
            ;;
        --lint-only)
            LINT_ONLY=true
            shift
            ;;
        --clean)
            CLEAN=true
            shift
            ;;
        *)
            echo "Opción desconocida: $1"
            show_help
            exit 1
            ;;
    esac
done

echo -e "${BLUE}🧪 Gustavo4Bot Test Runner${NC}"
echo "=================================="

# Verificar que estamos en el directorio correcto
if [[ ! -f "requirements.txt" ]] || [[ ! -d "tests" ]]; then
    echo -e "${RED}❌ Error: Ejecuta este script desde el directorio raíz del proyecto${NC}"
    exit 1
fi

# Limpiar archivos anteriores si se solicita
if [[ "$CLEAN" == true ]]; then
    echo -e "${YELLOW}🧹 Limpiando archivos de coverage anteriores...${NC}"
    rm -rf htmlcov/
    rm -f coverage.xml
    rm -f .coverage
    rm -f test-results.xml
fi

# Instalar dependencias si se solicita
if [[ "$INSTALL" == true ]]; then
    echo -e "${YELLOW}📦 Instalando dependencias...${NC}"
    pip install -r requirements.txt
    pip install -r requirements-test.txt
    pip install flake8 black isort mypy
fi

# Configurar variables de entorno para tests
export TELEGRAM_TOKEN="test_token_local"
export OWNER_ID="123456789"
export CHAT_SOURCE_ID="-1001234567890"
export PUBLISH_CHANNEL_ID="-1001234567891"
export STORAGE_CHANNEL_ID="-1001234567892"
export LOG_LEVEL="DEBUG"

# Solo linting
if [[ "$LINT_ONLY" == true ]]; then
    echo -e "${YELLOW}🔍 Ejecutando solo linting...${NC}"
    
    echo "📝 Verificando formato con black..."
    black --check bot tests || echo -e "${YELLOW}⚠️  Formato no óptimo (ejecuta: black bot tests)${NC}"
    
    echo "📋 Verificando imports con isort..."
    isort --check-only bot tests || echo -e "${YELLOW}⚠️  Imports no ordenados (ejecuta: isort bot tests)${NC}"
    
    echo "🔍 Linting con flake8..."
    flake8 bot tests --count --select=E9,F63,F7,F82 --show-source --statistics
    flake8 bot tests --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    echo "🔍 Type checking con mypy..."
    mypy bot --ignore-missing-imports || echo -e "${YELLOW}⚠️  Advertencias de tipos encontradas${NC}"
    
    echo -e "${GREEN}✅ Linting completado${NC}"
    exit 0
fi

# Preparar argumentos de pytest
PYTEST_ARGS=""

if [[ "$VERBOSE" == true ]]; then
    PYTEST_ARGS="$PYTEST_ARGS --verbose"
fi

if [[ "$COVERAGE" == true ]]; then
    PYTEST_ARGS="$PYTEST_ARGS --cov=bot --cov-report=term-missing --cov-report=html --cov-report=xml"
fi

if [[ "$FAST" == true ]]; then
    PYTEST_ARGS="$PYTEST_ARGS -m 'not slow'"
fi

# Ejecutar linting rápido
echo -e "${YELLOW}🔍 Linting rápido...${NC}"
flake8 bot tests --count --select=E9,F63,F7,F82 --show-source --statistics

# Ejecutar tests
echo -e "${YELLOW}🧪 Ejecutando tests...${NC}"
echo "Argumentos: pytest $PYTEST_ARGS"

if pytest $PYTEST_ARGS; then
    echo -e "${GREEN}✅ Todos los tests pasaron correctamente!${NC}"
    
    if [[ "$COVERAGE" == true ]]; then
        echo -e "${BLUE}📊 Reporte de coverage generado en htmlcov/index.html${NC}"
    fi
    
    # Mostrar resumen
    echo ""
    echo -e "${GREEN}🎉 ¡Éxito! El bot está listo para deployment${NC}"
    
else
    echo -e "${RED}❌ Algunos tests fallaron${NC}"
    echo -e "${YELLOW}💡 Revisa los errores arriba y corrige los problemas${NC}"
    exit 1
fi