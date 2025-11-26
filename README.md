# Aiken2QTI

Conversor de archivos Aiken a paquetes QTI 2.1 para importar en LMS (Canvas, Blackboard, Moodle, etc.)

## Características

- Convierte archivos de texto en formato Aiken a paquetes QTI 2.1 estándar
- Genera archivos XML válidos con estructura de preguntas de opción múltiple
- Crea manifesto IMS compatible
- Empaqueta todo en un archivo ZIP listo para importar
- Soporte completo para preguntas con múltiples opciones
- Identificadores únicos para evitar conflictos

## Instalación

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

## Uso

### Uso básico
```bash
python aiken2qti.py archivo_preguntas.txt
```

### Especificar archivo de salida
```bash
python aiken2qti.py archivo_preguntas.txt -o mi_examen.zip
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

## Desarrollo

### Ejecutar tests
```bash
pytest tests/
```

### Formatear código
```bash
black aiken2qti.py
```

### Análisis de código
```bash
flake8 aiken2qti.py
mypy aiken2qti.py
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

## Soporte

Si encuentras algún problema o tienes sugerencias, por favor abre un [issue](https://github.com/TiiZss/Aiken2QTI/issues).