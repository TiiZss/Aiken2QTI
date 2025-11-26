#!/usr/bin/env python3
"""
Script de automatización para desarrollo.

Facilita tareas comunes de desarrollo como formateo, testing, y análisis de código.
"""

import subprocess
import sys
from pathlib import Path
import argparse


def run_command(command, description=""):
    """Ejecuta un comando y retorna el resultado."""
    if description:
        print(f"🔧 {description}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr}")
        return False, e.stderr


def check_venv():
    """Verifica que el entorno virtual esté activo."""
    if sys.platform == "win32":
        python_path = Path("venv/Scripts/python.exe")
        pip_path = Path("venv/Scripts/pip.exe")
    else:
        python_path = Path("venv/bin/python")
        pip_path = Path("venv/bin/pip")
    
    if not python_path.exists():
        print("❌ Entorno virtual no encontrado. Ejecuta: python setup.py")
        return False
    
    return str(python_path), str(pip_path)


def format_code():
    """Formatea el código con black."""
    python_path, _ = check_venv()
    if not python_path:
        return False
    
    print("🎨 Formateando código con Black...")
    success, _ = run_command(f"{python_path} -m black aiken2qti.py")
    if success:
        print("✅ Código formateado correctamente")
    return success


def lint_code():
    """Analiza el código con flake8."""
    python_path, _ = check_venv()
    if not python_path:
        return False
    
    print("🔍 Analizando código con flake8...")
    success, output = run_command(f"{python_path} -m flake8 aiken2qti.py --max-line-length=88 --extend-ignore=E203,W503")
    if success and not output.strip():
        print("✅ No se encontraron problemas de estilo")
        return True
    elif output.strip():
        print("⚠️ Problemas de estilo encontrados:")
        print(output)
        return False
    return success


def type_check():
    """Verifica tipos con mypy."""
    python_path, _ = check_venv()
    if not python_path:
        return False
    
    print("🔬 Verificando tipos con mypy...")
    success, _ = run_command(f"{python_path} -m mypy aiken2qti.py")
    if success:
        print("✅ Verificación de tipos completada")
    return success


def run_tests():
    """Ejecuta las pruebas."""
    python_path, _ = check_venv()
    if not python_path:
        return False
    
    print("🧪 Ejecutando pruebas...")
    success, _ = run_command(f"{python_path} -m pytest test_aiken2qti.py -v")
    if success:
        print("✅ Todas las pruebas pasaron")
    return success


def run_tests_with_coverage():
    """Ejecuta las pruebas con cobertura."""
    python_path, _ = check_venv()
    if not python_path:
        return False
    
    print("🧪 Ejecutando pruebas con cobertura...")
    success, _ = run_command(f"{python_path} -m pytest test_aiken2qti.py --cov=aiken2qti --cov-report=html --cov-report=term")
    if success:
        print("✅ Pruebas completadas. Reporte en htmlcov/index.html")
    return success


def create_sample():
    """Crea un archivo de ejemplo."""
    python_path, _ = check_venv()
    if not python_path:
        return False
    
    print("📝 Creando archivo de ejemplo...")
    success, _ = run_command(f"{python_path} aiken2qti.py --create-sample ejemplo.txt")
    return success


def full_check():
    """Ejecuta todas las verificaciones."""
    print("🚀 VERIFICACIÓN COMPLETA")
    print("=" * 25)
    
    checks = [
        ("Formateo de código", format_code),
        ("Análisis de estilo", lint_code),
        ("Verificación de tipos", type_check),
        ("Pruebas unitarias", run_tests),
    ]
    
    results = []
    for name, func in checks:
        print(f"\n--- {name} ---")
        result = func()
        results.append((name, result))
    
    print(f"\n{'='*40}")
    print("📊 RESUMEN DE VERIFICACIONES")
    print("="*40)
    
    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {name}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 ¡Todas las verificaciones pasaron!")
        return True
    else:
        print("\n⚠️ Algunas verificaciones fallaron.")
        return False


def main():
    parser = argparse.ArgumentParser(description="Herramientas de desarrollo para Aiken2QTI")
    parser.add_argument("--format", action="store_true", help="Formatear código con Black")
    parser.add_argument("--lint", action="store_true", help="Analizar código con flake8")
    parser.add_argument("--type-check", action="store_true", help="Verificar tipos con mypy")
    parser.add_argument("--test", action="store_true", help="Ejecutar pruebas")
    parser.add_argument("--coverage", action="store_true", help="Ejecutar pruebas con cobertura")
    parser.add_argument("--sample", action="store_true", help="Crear archivo de ejemplo")
    parser.add_argument("--all", action="store_true", help="Ejecutar todas las verificaciones")
    
    args = parser.parse_args()
    
    # Verificar entorno virtual
    if not check_venv():
        return 1
    
    success = True
    
    if args.format:
        success &= format_code()
    
    if args.lint:
        success &= lint_code()
    
    if args.type_check:
        success &= type_check()
    
    if args.test:
        success &= run_tests()
    
    if args.coverage:
        success &= run_tests_with_coverage()
    
    if args.sample:
        success &= create_sample()
    
    if args.all:
        success = full_check()
    
    # Si no se especifica nada, mostrar ayuda
    if not any(vars(args).values()):
        parser.print_help()
        print(f"\n💡 Ejemplos de uso:")
        print(f"  python dev.py --format        # Formatear código")
        print(f"  python dev.py --test          # Ejecutar pruebas")
        print(f"  python dev.py --all           # Verificación completa")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())