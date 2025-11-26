#!/usr/bin/env python3
"""
Aiken2QTI - Convertidor de archivos Aiken a paquetes QTI 2.1

Este módulo convierte archivos de texto en formato Aiken a paquetes QTI 2.1
compatibles con LMS como Canvas, Blackboard, Moodle, etc.

Autor: TiiZss - Tomás Isasia
Versión: 2.0.0
Licencia: MIT
"""

import re
import uuid
import argparse
import os
import shutil
import zipfile
import xml.etree.ElementTree as ET
from xml.dom import minidom
import logging
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import sys
from dataclasses import dataclass

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@dataclass
class Question:
    """Representa una pregunta con sus opciones y respuesta correcta."""

    text: str
    options: Dict[str, str]
    answer: str

    def __post_init__(self):
        """Valida la pregunta después de la inicialización."""
        if not self.text.strip():
            raise ValueError("El texto de la pregunta no puede estar vacío")
        if not self.options:
            raise ValueError("La pregunta debe tener al menos una opción")
        if self.answer not in self.options:
            raise ValueError(
                f"La respuesta '{self.answer}' no está entre las opciones disponibles: {list(self.options.keys())}"
            )


class AikenParser:
    """Parser para archivos en formato Aiken."""

    def __init__(self):
        self.option_pattern = re.compile(r"^([A-Z])[\)\.]\s+(.+)$")
        self.answer_pattern = re.compile(r"^ANSWER:\s*([A-Z])$", re.IGNORECASE)

    def parse_file(self, file_path: Path) -> List[Question]:
        """
        Lee un archivo Aiken y retorna una lista de preguntas.

        Args:
            file_path: Ruta al archivo Aiken

        Returns:
            Lista de objetos Question

        Raises:
            FileNotFoundError: Si el archivo no existe
            ValueError: Si el formato es inválido
        """
        if not file_path.exists():
            raise FileNotFoundError(f"El archivo {file_path} no existe")

        logger.info(f"Parseando archivo: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f.readlines()]
        except UnicodeDecodeError:
            logger.error(
                f"Error de codificación en {file_path}. Intentando con latin-1..."
            )
            try:
                with open(file_path, "r", encoding="latin-1") as f:
                    lines = [line.strip() for line in f.readlines()]
            except Exception as e:
                raise ValueError(f"No se pudo leer el archivo {file_path}: {e}")

        questions = []
        current_question_text = ""
        current_options = {}
        line_number = 0

        for line in lines:
            line_number += 1

            if not line:  # Línea vacía
                continue

            # Verificar si es una respuesta
            answer_match = self.answer_pattern.match(line)
            if answer_match:
                answer = answer_match.group(1).upper()

                if not current_question_text:
                    logger.warning(
                        f"Línea {line_number}: ANSWER encontrado sin pregunta previa"
                    )
                    continue

                if not current_options:
                    logger.warning(
                        f"Línea {line_number}: ANSWER encontrado sin opciones"
                    )
                    continue

                try:
                    question = Question(
                        text=current_question_text.strip(),
                        options=current_options.copy(),
                        answer=answer,
                    )
                    questions.append(question)
                    logger.debug(f"Pregunta {len(questions)} parseada correctamente")
                except ValueError as e:
                    logger.error(f"Error en pregunta línea {line_number}: {e}")

                # Reset para la siguiente pregunta
                current_question_text = ""
                current_options = {}
                continue

            # Verificar si es una opción
            option_match = self.option_pattern.match(line)
            if option_match:
                option_letter = option_match.group(1)
                option_text = option_match.group(2)
                current_options[option_letter] = option_text
                continue

            # Si no es ANSWER ni opción, es parte del texto de la pregunta
            if current_question_text:
                current_question_text += " " + line
            else:
                current_question_text = line

        # Verificar si quedó una pregunta sin ANSWER
        if current_question_text or current_options:
            logger.warning("Pregunta incompleta al final del archivo (falta ANSWER)")

        logger.info(f"Parseado completado: {len(questions)} preguntas encontradas")
        return questions


class QTIGenerator:
    """Generador de archivos QTI 2.1."""

    def __init__(self):
        self.qti_ns = "http://www.imsglobal.org/xsd/imsqti_v2p1"
        self.imscp_ns = "http://www.imsglobal.org/xsd/imscp_v1p1"

    def generate_item_xml(self, question: Question, item_id: str) -> str:
        """
        Genera el XML de una pregunta individual (AssessmentItem).

        Args:
            question: Objeto Question con los datos de la pregunta
            item_id: Identificador único para la pregunta

        Returns:
            String con el XML generado
        """
        root = ET.Element(
            "assessmentItem",
            {
                "xmlns": self.qti_ns,
                "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                "xsi:schemaLocation": f"{self.qti_ns} {self.qti_ns.replace('xsd/', 'xsd/')}.xsd",
                "identifier": item_id,
                "title": self._safe_title(question.text),
                "adaptive": "false",
                "timeDependent": "false",
            },
        )

        # Response Declaration
        response_decl = ET.SubElement(
            root,
            "responseDeclaration",
            {
                "identifier": "RESPONSE",
                "cardinality": "single",
                "baseType": "identifier",
            },
        )

        correct_response = ET.SubElement(response_decl, "correctResponse")

        # Generar IDs únicos para las opciones
        option_ids = {
            letter: f"Choice_{letter}_{uuid.uuid4().hex[:8]}"
            for letter in question.options.keys()
        }

        # Establecer la respuesta correcta
        if question.answer in option_ids:
            value_elem = ET.SubElement(correct_response, "value")
            value_elem.text = option_ids[question.answer]

        # Outcome Declaration
        outcome_decl = ET.SubElement(
            root,
            "outcomeDeclaration",
            {"identifier": "SCORE", "cardinality": "single", "baseType": "float"},
        )
        default_value = ET.SubElement(outcome_decl, "defaultValue")
        value_elem = ET.SubElement(default_value, "value")
        value_elem.text = "0"

        # Item Body
        item_body = ET.SubElement(root, "itemBody")

        # Texto de la pregunta
        div_elem = ET.SubElement(item_body, "div")
        p_elem = ET.SubElement(div_elem, "p")
        p_elem.text = question.text

        # Choice Interaction
        choice_interaction = ET.SubElement(
            item_body,
            "choiceInteraction",
            {"responseIdentifier": "RESPONSE", "shuffle": "true", "maxChoices": "1"},
        )

        # Prompt opcional
        prompt = ET.SubElement(choice_interaction, "prompt")
        prompt.text = "Selecciona la respuesta correcta:"

        # Opciones de respuesta
        for letter in sorted(question.options.keys()):
            text = question.options[letter]
            simple_choice = ET.SubElement(
                choice_interaction, "simpleChoice", {"identifier": option_ids[letter]}
            )
            simple_choice.text = text

        # Response Processing
        self._add_response_processing(root)

        # Convertir a string con formato
        rough_string = ET.tostring(root, encoding="unicode")
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def _safe_title(self, text: str, max_length: int = 50) -> str:
        """Genera un título seguro para el XML."""
        # Limpiar caracteres problemáticos
        safe_text = re.sub(r'[<>&"]', "", text)
        if len(safe_text) > max_length:
            safe_text = safe_text[:max_length] + "..."
        return safe_text or "Pregunta sin título"

    def _add_response_processing(self, root: ET.Element) -> None:
        """Añade el procesamiento de respuestas al XML."""
        rp = ET.SubElement(
            root,
            "responseProcessing",
            {
                "template": "http://www.imsglobal.org/question/qti_v2p1/rptemplates/match_correct"
            },
        )

    def generate_manifest(self, resources: List[Tuple[str, str]]) -> str:
        """
        Genera el imsmanifest.xml que lista todos los recursos.

        Args:
            resources: Lista de tuplas (id, filename)

        Returns:
            String con el XML del manifest
        """
        root = ET.Element(
            "manifest",
            {
                "xmlns": self.imscp_ns,
                "xmlns:imsmd": "http://www.imsglobal.org/xsd/imsmd_v1p2",
                "xmlns:imsqti": self.qti_ns,
                "identifier": f"MANIFEST-{uuid.uuid4().hex}",
                "version": "1.0",
            },
        )

        # Metadata
        metadata = ET.SubElement(root, "metadata")
        schema = ET.SubElement(metadata, "schema")
        schema.text = "IMS Content"
        schema_version = ET.SubElement(metadata, "schemaversion")
        schema_version.text = "1.1.3"

        # Metadata adicional
        imsmd_lom = ET.SubElement(metadata, "imsmd:lom")
        general = ET.SubElement(imsmd_lom, "imsmd:general")
        title = ET.SubElement(general, "imsmd:title")
        langstring = ET.SubElement(title, "imsmd:langstring", {"xml:lang": "es"})
        langstring.text = "Cuestionario Aiken2QTI"

        # Organizations
        organizations = ET.SubElement(root, "organizations")

        # Resources
        resources_elem = ET.SubElement(root, "resources")

        for res_id, filename in resources:
            resource = ET.SubElement(
                resources_elem,
                "resource",
                {
                    "identifier": f"RES-{res_id}",
                    "type": "imsqti_item_xmlv2p1",
                    "href": filename,
                },
            )

            file_elem = ET.SubElement(resource, "file", {"href": filename})

        # Formatear y retornar
        rough_string = ET.tostring(root, encoding="unicode")
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")


class PackageBuilder:
    """Constructor de paquetes QTI."""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.temp_dir = output_dir / "temp_qti_build"

    def build_package(self, questions: List[Question], output_filename: str) -> Path:
        """
        Construye el paquete QTI completo.

        Args:
            questions: Lista de preguntas
            output_filename: Nombre del archivo ZIP de salida

        Returns:
            Path al archivo ZIP generado
        """
        logger.info(f"Construyendo paquete QTI con {len(questions)} preguntas")

        # Limpiar y crear directorio temporal
        self._setup_temp_directory()

        try:
            generator = QTIGenerator()
            resources = []

            # Generar archivos XML para cada pregunta
            for index, question in enumerate(questions, 1):
                item_id = f"ITEM_{uuid.uuid4().hex}"
                filename = f"question_{index:03d}_{item_id}.xml"

                # Generar XML
                xml_content = generator.generate_item_xml(question, item_id)

                # Guardar archivo
                xml_path = self.temp_dir / filename
                with open(xml_path, "w", encoding="utf-8") as f:
                    f.write(xml_content)

                resources.append((item_id, filename))
                logger.debug(f"Generado: {filename}")

            # Generar manifest
            manifest_content = generator.generate_manifest(resources)
            manifest_path = self.temp_dir / "imsmanifest.xml"
            with open(manifest_path, "w", encoding="utf-8") as f:
                f.write(manifest_content)

            # Crear ZIP
            output_path = self._create_zip_package(output_filename)

            logger.info(f"Paquete QTI creado exitosamente: {output_path}")
            return output_path

        finally:
            # Limpiar directorio temporal
            self._cleanup_temp_directory()

    def _setup_temp_directory(self) -> None:
        """Configura el directorio temporal."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Directorio temporal creado: {self.temp_dir}")

    def _cleanup_temp_directory(self) -> None:
        """Limpia el directorio temporal."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            logger.debug("Directorio temporal eliminado")

    def _create_zip_package(self, output_filename: str) -> Path:
        """Crea el archivo ZIP con el paquete QTI."""
        if not output_filename.endswith(".zip"):
            output_filename += ".zip"

        output_path = self.output_dir / output_filename

        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in self.temp_dir.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(self.temp_dir)
                    zipf.write(file_path, arcname)
                    logger.debug(f"Añadido al ZIP: {arcname}")

        return output_path


def create_sample_file(output_path: Path) -> None:
    """Crea un archivo de ejemplo en formato Aiken."""
    sample_content = """¿Cuál es la capital de Francia?
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

¿Cuál es el resultado de 2 + 2?
A) 3
B) 4
C) 5
D) 6
ANSWER: B

¿En qué año llegó Cristóbal Colón a América?
A) 1490
B) 1491
C) 1492
D) 1493
ANSWER: C

¿Cuál es el océano más grande del mundo?
A) Atlántico
B) Índico
C) Ártico
D) Pacífico
ANSWER: D
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(sample_content)

    logger.info(f"Archivo de ejemplo creado: {output_path}")


def validate_input_file(file_path: Path) -> None:
    """Valida que el archivo de entrada sea válido."""
    if not file_path.exists():
        raise FileNotFoundError(f"El archivo {file_path} no existe")

    if not file_path.is_file():
        raise ValueError(f"{file_path} no es un archivo válido")

    if file_path.stat().st_size == 0:
        raise ValueError(f"El archivo {file_path} está vacío")


def setup_logging(verbose: bool = False) -> None:
    """Configura el sistema de logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main() -> int:
    """Función principal del programa."""
    parser = argparse.ArgumentParser(
        description="Convierte archivos Aiken a paquetes QTI 2.1 compatibles con LMS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python aiken2qti.py preguntas.txt
  python aiken2qti.py preguntas.txt -o mi_examen.zip
  python aiken2qti.py --create-sample ejemplo.txt
  python aiken2qti.py preguntas.txt --verbose

Formato Aiken esperado:
  ¿Pregunta aquí?
  A) Opción 1
  B) Opción 2  
  C) Opción 3
  D) Opción 4
  ANSWER: B
        """,
    )

    parser.add_argument("input_file", nargs="?", help="Archivo .txt en formato Aiken")

    parser.add_argument(
        "--output",
        "-o",
        default="paquete_qti.zip",
        help="Nombre del archivo ZIP de salida (default: paquete_qti.zip)",
    )

    parser.add_argument(
        "--create-sample",
        metavar="FILENAME",
        help="Crear un archivo de ejemplo en formato Aiken",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Mostrar información detallada de debug",
    )

    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Solo validar el archivo sin generar el paquete QTI",
    )

    args = parser.parse_args()

    # Configurar logging
    setup_logging(args.verbose)

    try:
        # Crear archivo de ejemplo si se solicita
        if args.create_sample:
            sample_path = Path(args.create_sample)
            create_sample_file(sample_path)
            print(f"✅ Archivo de ejemplo creado: {sample_path}")
            return 0

        # Validar argumentos
        if not args.input_file:
            parser.error(
                "Se requiere especificar un archivo de entrada o usar --create-sample"
            )

        input_path = Path(args.input_file)
        output_dir = Path.cwd()

        # Validar archivo de entrada
        validate_input_file(input_path)

        # Parsear archivo Aiken
        logger.info("=== INICIANDO CONVERSIÓN AIKEN -> QTI 2.1 ===")
        parser_instance = AikenParser()
        questions = parser_instance.parse_file(input_path)

        if not questions:
            logger.error("❌ No se encontraron preguntas válidas en el archivo")
            return 1

        print(f"📝 Preguntas encontradas: {len(questions)}")

        # Solo validar si se solicita
        if args.validate_only:
            print("✅ Archivo validado correctamente")
            for i, q in enumerate(questions, 1):
                print(f"  {i}. {q.text[:60]}{'...' if len(q.text) > 60 else ''}")
            return 0

        # Construir paquete QTI
        builder = PackageBuilder(output_dir)
        output_path = builder.build_package(questions, args.output)

        # Mostrar resultados
        print("\n=== CONVERSIÓN COMPLETADA ===")
        print(f"✅ Archivo generado: {output_path}")
        print(f"📦 Tamaño: {output_path.stat().st_size / 1024:.1f} KB")
        print(f"📊 Preguntas procesadas: {len(questions)}")
        print("\n💡 Puedes importar este archivo ZIP en:")
        print("   • Canvas")
        print("   • Blackboard")
        print("   • Moodle")
        print("   • D2L Brightspace")
        print("   • Schoology")
        print("   • Otros LMS compatibles con QTI 2.1")

        return 0

    except FileNotFoundError as e:
        logger.error(f"❌ Archivo no encontrado: {e}")
        return 1
    except ValueError as e:
        logger.error(f"❌ Error de validación: {e}")
        return 1
    except Exception as e:
        logger.error(f"❌ Error inesperado: {e}")
        if args.verbose:
            logger.exception("Detalles del error:")
        return 1


if __name__ == "__main__":
    sys.exit(main())
