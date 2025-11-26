# Contributing to Aiken2QTI

¡Gracias por tu interés en contribuir a Aiken2QTI! 🎉

## Cómo contribuir

### Reportar bugs

Si encuentras un error:

1. Verifica que no esté ya reportado en [Issues](https://github.com/TiiZss/Aiken2QTI/issues)
2. Crea un nuevo issue con:
   - Descripción clara del problema
   - Pasos para reproducirlo
   - Comportamiento esperado vs actual
   - Información del sistema (OS, versión Python)
   - Archivo Aiken de ejemplo (si aplica)

### Sugerir mejoras

Para proponer nuevas funcionalidades:

1. Abre un issue con la etiqueta "enhancement"
2. Describe claramente el problema que resuelve
3. Explica la solución propuesta
4. Considera alternativas

### Desarrollo

#### Configuración del entorno

```bash
# 1. Fork del repositorio en GitHub
# 2. Clonar tu fork
git clone https://github.com/TU_USUARIO/Aiken2QTI.git
cd Aiken2QTI

# 3. Configurar entorno
python setup.py --dev

# 4. Activar entorno virtual
.\activate.ps1  # Windows PowerShell
# o
source venv/bin/activate  # Linux/macOS
```

#### Flujo de trabajo

1. **Crear una rama para tu feature:**
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```

2. **Desarrollar y hacer commit:**
   ```bash
   # Hacer cambios...
   git add .
   git commit -m "Add nueva funcionalidad"
   ```

3. **Ejecutar verificaciones:**
   ```bash
   python dev.py --all
   ```

4. **Push y Pull Request:**
   ```bash
   git push origin feature/nueva-funcionalidad
   ```
   Luego abre un Pull Request en GitHub.

#### Estándares de código

- **Formateo:** Usa Black (`python dev.py --format`)
- **Linting:** Debe pasar flake8 (`python dev.py --lint`)
- **Tipos:** Usa type hints y verifica con mypy (`python dev.py --type-check`)
- **Tests:** Añade tests para nuevas funcionalidades (`python dev.py --test`)
- **Documentación:** Documenta funciones públicas con docstrings

#### Estructura de commits

Usa mensajes de commit descriptivos:

```
Add: nueva funcionalidad
Fix: corrección de bug
Update: actualización de dependencias
Docs: mejoras en documentación
Test: añadir o modificar tests
Refactor: refactoring sin cambios funcionales
```

## Áreas donde puedes contribuir

### 🐛 Corrección de errores
- Manejo de archivos con codificaciones especiales
- Validación de formatos Aiken complejos
- Compatibilidad con diferentes versiones de Python

### ✨ Nuevas funcionalidades
- Soporte para más tipos de preguntas (verdadero/falso, respuesta corta)
- Interfaz gráfica de usuario
- Conversión desde otros formatos
- Export a otros formatos estándar

### 📚 Documentación
- Ejemplos de uso avanzados
- Tutoriales en video
- Traducción a otros idiomas
- Mejoras en README y wikis

### 🧪 Testing
- Tests con casos edge
- Tests de integración con LMS reales
- Performance testing
- Compatibility testing

### 🎨 UX/UI
- Mejoras en la interfaz de línea de comandos
- Mensajes de error más claros
- Progress bars para archivos grandes
- Colored output

## Revisión de Pull Requests

Todos los PRs serán revisados considerando:

- ✅ Funcionalidad correcta
- ✅ Tests pasan
- ✅ Código formateado
- ✅ Documentación actualizada
- ✅ No introduce regresiones
- ✅ Sigue las convenciones del proyecto

## Código de Conducta

Mantén un ambiente respetuoso y profesional. Lee nuestro [Código de Conducta](CODE_OF_CONDUCT.md).

## Licencia

Al contribuir, aceptas que tus contribuciones sean licenciadas bajo la [MIT License](LICENSE).

---

¡Gracias por ayudar a hacer Aiken2QTI mejor! 🚀