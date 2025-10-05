# Configuración de Branch Protection para PRs

Este documento explica cómo configurar la protección de rama para que GitHub requiera que pasen todos los tests antes de permitir el merge de PRs.

## ⚙️ Configuración Automática (Recomendado)

### Usando GitHub CLI:

```bash
# Configurar protección de rama main
gh api repos/:owner/:repo/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["PR Status Check"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true}' \
  --field restrictions=null

# Para el repositorio actual (ejecutar desde la carpeta del repo):
gh api repos/davidperezmillan/CdO/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["PR Status Check"]}' \
  --field enforce_admins=false \
  --field required_pull_request_reviews='{"required_approving_review_count":0,"dismiss_stale_reviews":false}' \
  --field restrictions=null
```

## 🖱️ Configuración Manual

Si prefieres configurarlo desde la interfaz web de GitHub:

1. Ve a tu repositorio en GitHub
2. Ve a **Settings** > **Branches**
3. Click en **Add rule** o edita la regla existente para `main`
4. Configura estas opciones:

### ✅ Opciones Obligatorias:
- ☑️ **Require status checks to pass before merging**
  - ☑️ **Require branches to be up to date before merging**
  - En "Status checks found in the last week for this repository":
    - ☑️ **PR Status Check** (este es el job crítico)
    - ☑️ **Quality Gate** (opcional, pero recomendado)

### 🔒 Opciones Recomendadas:
- ☑️ **Require a pull request before merging**
  - ☑️ **Dismiss stale PR reviews when new commits are pushed**
- ☑️ **Require conversation resolution before merging**
- ☑️ **Do not allow bypassing the above settings** (para enforcing estricto)

### ⚠️ Opciones según tu equipo:
- **Restrict pushes to matching branches** (solo si quieres limitar quién puede hacer push)
- **Require signed commits** (si tu equipo usa commit signing)

## 🎯 Verificación

Para verificar que funciona correctamente:

1. Crea una nueva rama: `git checkout -b test-pr-protection`
2. Haz un cambio que rompa los tests
3. Haz commit y push
4. Crea un PR
5. Verifica que GitHub muestra "Some checks haven't completed yet" o "Some checks were not successful"
6. El botón "Merge pull request" debe estar deshabilitado

## 🔧 Status Checks Incluidos

El workflow `pr-quality-gate.yml` incluye estos checks que deben pasar:

| Check | Descripción | Bloquea Merge |
|-------|-------------|---------------|
| **Code Formatting** | Verifica formato con black | ✅ Sí |
| **Import Sorting** | Verifica orden de imports con isort | ✅ Sí |
| **Critical Linting** | Errores críticos de flake8 | ✅ Sí |
| **Test Suite** | Todos los tests deben pasar | ✅ Sí |
| **Test Coverage** | Mínimo 70% de cobertura | ✅ Sí |
| **Security Scan** | Verificación básica de seguridad | ✅ Sí |
| **Type Checking** | Verificación de tipos con mypy | ⚠️ Warning only |
| **Code Quality** | Warnings adicionales de flake8 | ⚠️ Warning only |

## 🚀 Flujo de Trabajo

Con esta configuración, el flujo para PRs será:

1. **Desarrollador crea PR** → Workflow se ejecuta automáticamente
2. **Tests fallan** → Merge bloqueado, GitHub muestra error
3. **Desarrollador arregla issues** → Push activar re-check automático  
4. **Tests pasan** → Merge habilitado ✅
5. **Merge realizado** → Workflow de deploy se ejecuta

## 🔄 Comandos Útiles para Desarrolladores

```bash
# Verificar formato antes de commit
black --check bot tests
isort --check-only bot tests
flake8 bot tests --select=E9,F63,F7,F82

# Arreglar formato automáticamente
black bot tests
isort bot tests

# Ejecutar tests localmente
pytest --cov=bot --cov-report=term-missing

# Verificar todo de una vez
./run-tests.sh  # (si existe el script)
```

## 🎉 Beneficios

- ✅ **Calidad garantizada**: No se puede mergear código que rompe tests
- ✅ **Formato consistente**: Todo el código sigue las mismas reglas  
- ✅ **Detección temprana**: Problemas encontrados antes del merge
- ✅ **CI/CD confiable**: Deploy solo ocurre con código que funciona
- ✅ **Colaboración mejorada**: Reviews focalizados en lógica, no formato

---

**Nota**: Después de configurar la protección, solo los PRs nuevos estarán sujetos a estas reglas. Los pushes directos a main (si están permitidos) seguirán funcionando normalmente.