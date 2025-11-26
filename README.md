# Aiken2QTI

[![CI/CD Pipeline](https://github.com/TiiZss/Aiken2QTI/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/TiiZss/Aiken2QTI/actions)
[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub Issues](https://img.shields.io/github/issues/TiiZss/Aiken2QTI)](https://github.com/TiiZss/Aiken2QTI/issues)
[![GitHub Stars](https://img.shields.io/github/stars/TiiZss/Aiken2QTI)](https://github.com/TiiZss/Aiken2QTI/stargazers)

Conversor de archivos Aiken a paquetes QTI 2.1 para importar en LMS (Canvas, Blackboard, Moodle, etc.)

## Características

- Convierte archivos de texto en formato Aiken a paquetes QTI 2.1 estándar
- Genera archivos XML válidos con estructura de preguntas de opción múltiple
- Crea manifesto IMS compatible
- Empaqueta todo en un archivo ZIP listo para importar
- Soporte completo para preguntas con múltiples opciones
- Identificadores únicos para evitar conflictos

## 🚀 Instalación Rápida

### Instalación automática (recomendada)

**Windows (PowerShell):**
```powershell
git clone https://github.com/TiiZss/Aiken2QTI.git
cd Aiken2QTI
python setup.py --dev
.\activate.ps1
```

**Windows (CMD):**
```cmd
git clone https://github.com/TiiZss/Aiken2QTI.git
cd Aiken2QTI
python setup.py --dev
activate.bat
```

**Linux/macOS:**
```bash
git clone https://github.com/TiiZss/Aiken2QTI.git
cd Aiken2QTI
python setup.py --dev
source venv/bin/activate
```

### Instalación manual

### 1. Clonar el repositorio
```bash
git clone https://github.com/TiiZss/Aiken2QTI.git
cd Aiken2QTI
```

### 2. Crear entorno virtual
```bash
python -m venv venv
```

### 3. Activar entorno virtual
**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

## 💡 Uso

### Crear archivo de ejemplo
```bash
python aiken2qti.py --create-sample mis_preguntas.txt
```

### Uso básico
```bash
python aiken2qti.py archivo_preguntas.txt
```

### Especificar archivo de salida
```bash
python aiken2qti.py archivo_preguntas.txt -o mi_examen.zip
```

### Validar archivo sin convertir
```bash
python aiken2qti.py archivo_preguntas.txt --validate-only
```

### Modo verbose (para debugging)
```bash
python aiken2qti.py archivo_preguntas.txt --verbose
```

### Ver ayuda completa
```bash
python aiken2qti.py --help
```

### Ejemplo de archivo Aiken

```
¿Cuál es la capital de Francia?
A) Londres
B) París
C) Madrid
D) Roma
ANSWER: B

¿Cuántos días tiene una semana?
A) 5
B) 6
C) 7
D) 8
ANSWER: C
```

## Formato de archivo Aiken

- Cada pregunta comienza con el texto de la pregunta
- Las opciones se marcan con letras seguidas de `)` o `.`
- La respuesta correcta se indica con `ANSWER: [LETRA]`
- Las preguntas se separan con líneas en blanco

## 🔧 Desarrollo

### Setup del entorno de desarrollo
```bash
python setup.py --dev  # Instala dependencias de desarrollo
```

### Herramientas de desarrollo (script automatizado)
```bash
# Verificación completa
python dev.py --all

# Herramientas individuales
python dev.py --format      # Formatear código
python dev.py --lint        # Análisis de código
python dev.py --type-check  # Verificación de tipos
python dev.py --test        # Ejecutar pruebas
python dev.py --coverage    # Pruebas con cobertura
```

### Comandos individuales

#### Ejecutar tests
```bash
pytest test_aiken2qti.py -v
```

#### Formatear código
```bash
black aiken2qti.py
```

#### Análisis de código
```bash
flake8 aiken2qti.py --max-line-length=88
mypy aiken2qti.py
```

#### Cobertura de tests
```bash
pytest test_aiken2qti.py --cov=aiken2qti --cov-report=html
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Compatibilidad

- **Canvas**: ✅ Compatible
- **Blackboard**: ✅ Compatible  
- **Moodle**: ✅ Compatible
- **D2L Brightspace**: ✅ Compatible
- **Schoology**: ✅ Compatible

## ⭐ Características Avanzadas

- **🏗️ Arquitectura robusta**: Código orientado a objetos con manejo de errores completo
- **🧪 Tests automáticos**: Suite completa de pruebas unitarias e integración
- **🔧 Herramientas de desarrollo**: Formateo, linting y verificación de tipos automáticos
- **📊 CI/CD Pipeline**: Tests automáticos en múltiples versiones de Python (3.7-3.11)
- **📚 Documentación completa**: Guías para usuarios y contribuyentes
- **🌍 Multiplataforma**: Compatible con Windows, macOS y Linux
- **🚀 Setup automatizado**: Scripts de configuración y activación incluidos

## 📈 Estado del Proyecto

- ✅ **Estable**: Listo para uso en producción
- ✅ **Mantenido activamente**: Updates y mejoras regulares
- ✅ **Código de calidad**: 100% type hints, tests y documentación
- ✅ **Comunidad**: Contribuciones bienvenidas

## Soporte

Si encuentras algún problema o tienes sugerencias, por favor abre un [issue](https://github.com/TiiZss/Aiken2QTI/issues).