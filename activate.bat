@echo off
echo.
echo ==========================
echo   AIKEN2QTI - Activacion
echo ==========================
echo.

REM Verificar si existe el entorno virtual
if not exist "venv\" (
    echo ❌ Entorno virtual no encontrado
    echo.
    echo Ejecuta primero: python setup.py
    echo.
    pause
    exit /b 1
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

echo ✅ Entorno virtual activado
echo.
echo 💡 Comandos disponibles:
echo    python aiken2qti.py archivo.txt        # Convertir archivo
echo    python aiken2qti.py --create-sample    # Crear ejemplo
echo    python dev.py --test                   # Ejecutar pruebas
echo    python dev.py --all                    # Verificación completa
echo.
echo Para desactivar el entorno: deactivate
echo.

REM Mantener la ventana abierta
cmd /k