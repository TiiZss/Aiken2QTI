#!/usr/bin/env python3
"""
Script de configuración y activación del entorno virtual.

Uso:
  python setup.py          # Instalar dependencias
  python setup.py --clean  # Limpiar y reinstalar
  python setup.py --dev    # Instalar dependencias de desarrollo
"""

import subprocess
import sys
import os
from pathlib import Path
import argparse


def run_command(command, shell=True):
    """Ejecuta un comando y maneja errores."""
    try:
        result = subprocess.run(
            command,
            shell=shell,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ {command}")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando: {command}")
        print(f"Error: {e.stderr}")
        return False


def check_python_version():
    """Verifica que Python sea >= 3.7."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Se requiere Python 3.7 o superior")
        print(f"Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def create_venv():
    """Crea el entorno virtual si no existe."""
    venv_path = Path("venv")
    if venv_path.exists():
        print("✅ Entorno virtual ya existe")
        return True
    
    print("📦 Creando entorno virtual...")
    return run_command("python -m venv venv")


def get_activation_script():
    """Retorna el script de activación según el OS."""
    if sys.platform == "win32":
        return "venv\\Scripts\\activate.bat"
    return "source venv/bin/activate"


def install_packages(dev=False):
    """Instala las dependencias."""
    if sys.platform == "win32":
        pip_cmd = "venv\\Scripts\\pip"
    else:
        pip_cmd = "venv/bin/pip"
    
    # Actualizar pip
    print("📦 Actualizando pip...")
    if not run_command(f"{pip_cmd} install --upgrade pip"):
        return False
    
    # Instalar dependencias básicas
    print("📦 Instalando dependencias...")
    if not run_command(f"{pip_cmd} install -r requirements.txt"):
        return False
    
    # Instalar dependencias de desarrollo si se solicita
    if dev:
        dev_packages = [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0", 
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0"
        ]
        for package in dev_packages:
            print(f"📦 Instalando {package}...")
            if not run_command(f"{pip_cmd} install {package}"):
                return False
    
    return True


def clean_environment():
    """Limpia el entorno virtual."""
    import shutil
    venv_path = Path("venv")
    if venv_path.exists():
        print("🧹 Limpiando entorno virtual...")
        shutil.rmtree(venv_path)
        print("✅ Entorno virtual eliminado")


def show_usage_info():
    """Muestra información de uso."""
    activation_script = get_activation_script()
    
    print("\n" + "="*50)
    print("🎉 ¡CONFIGURACIÓN COMPLETADA!")
    print("="*50)
    print(f"\n📝 Para activar el entorno virtual:")
    if sys.platform == "win32":
        print(f"   {activation_script}")
        print("   # O en PowerShell:")
        print("   .\\venv\\Scripts\\Activate.ps1")
    else:
        print(f"   {activation_script}")
    
    print(f"\n🚀 Para ejecutar el programa:")
    print("   python aiken2qti.py archivo.txt")
    print("   python aiken2qti.py --create-sample ejemplo.txt")
    
    print(f"\n🧪 Para ejecutar tests (si instalaste dependencias de dev):")
    print("   pytest test_aiken2qti.py -v")
    
    print(f"\n🎨 Para formatear código:")
    print("   black aiken2qti.py")
    
    print(f"\n📊 Para análisis de código:")
    print("   flake8 aiken2qti.py")
    print("   mypy aiken2qti.py")


def main():
    parser = argparse.ArgumentParser(description="Configurador del entorno Aiken2QTI")
    parser.add_argument("--clean", action="store_true", help="Limpiar entorno antes de instalar")
    parser.add_argument("--dev", action="store_true", help="Instalar dependencias de desarrollo")
    
    args = parser.parse_args()
    
    print("🔧 CONFIGURACIÓN DE AIKEN2QTI")
    print("=" * 35)
    
    # Verificar Python
    if not check_python_version():
        return 1
    
    # Limpiar si se solicita
    if args.clean:
        clean_environment()
    
    # Crear entorno virtual
    if not create_venv():
        return 1
    
    # Instalar dependencias
    if not install_packages(dev=args.dev):
        return 1
    
    # Mostrar información de uso
    show_usage_info()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())