# Script de activación para PowerShell
# Uso: .\activate.ps1

Write-Host ""
Write-Host "==========================" -ForegroundColor Cyan
Write-Host "   AIKEN2QTI - Activación" -ForegroundColor Cyan  
Write-Host "==========================" -ForegroundColor Cyan
Write-Host ""

# Verificar si existe el entorno virtual
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "❌ Entorno virtual no encontrado" -ForegroundColor Red
    Write-Host ""
    Write-Host "Ejecuta primero: python setup.py" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Presiona Enter para continuar"
    exit 1
}

# Activar entorno virtual
& ".\venv\Scripts\Activate.ps1"

Write-Host "✅ Entorno virtual activado" -ForegroundColor Green
Write-Host ""
Write-Host "💡 Comandos disponibles:" -ForegroundColor Yellow
Write-Host "   python aiken2qti.py archivo.txt        # Convertir archivo"
Write-Host "   python aiken2qti.py --create-sample    # Crear ejemplo"  
Write-Host "   python dev.py --test                   # Ejecutar pruebas"
Write-Host "   python dev.py --all                    # Verificación completa"
Write-Host ""
Write-Host "Para desactivar el entorno: deactivate" -ForegroundColor Cyan
Write-Host ""