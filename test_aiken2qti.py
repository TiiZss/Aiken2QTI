#!/usr/bin/env python3
"""
Pruebas unitarias para aiken2qti.py

Ejecutar con: pytest test_aiken2qti.py -v
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import zipfile
import xml.etree.ElementTree as ET

from aiken2qti import AikenParser, Question, QTIGenerator, PackageBuilder


class TestQuestion:
    """Tests para la clase Question."""
    
    def test_question_creation_valid(self):
        """Test creación válida de pregunta."""
        q = Question(
            text="¿Cuál es la capital de Francia?",
            options={"A": "Londres", "B": "París", "C": "Madrid"},
            answer="B"
        )
        assert q.text == "¿Cuál es la capital de Francia?"
        assert q.answer == "B"
        assert len(q.options) == 3
    
    def test_question_empty_text(self):
        """Test pregunta con texto vacío."""
        with pytest.raises(ValueError, match="texto de la pregunta no puede estar vacío"):
            Question(
                text="",
                options={"A": "Opción 1"},
                answer="A"
            )
    
    def test_question_no_options(self):
        """Test pregunta sin opciones."""
        with pytest.raises(ValueError, match="debe tener al menos una opción"):
            Question(
                text="Pregunta test",
                options={},
                answer="A"
            )
    
    def test_question_invalid_answer(self):
        """Test pregunta con respuesta inválida."""
        with pytest.raises(ValueError, match="no está entre las opciones disponibles"):
            Question(
                text="Pregunta test",
                options={"A": "Opción 1", "B": "Opción 2"},
                answer="C"
            )


class TestAikenParser:
    """Tests para el parser Aiken."""
    
    def setup_method(self):
        """Configuración para cada test."""
        self.parser = AikenParser()
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def create_temp_file(self, content: str) -> Path:
        """Crea un archivo temporal con el contenido dado."""
        temp_file = self.temp_dir / "test.txt"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(content)
        return temp_file
    
    def test_parse_single_question(self):
        """Test parsing de una sola pregunta."""
        content = """¿Cuál es la capital de Francia?
A) Londres
B) París
C) Madrid
ANSWER: B"""
        
        file_path = self.create_temp_file(content)
        questions = self.parser.parse_file(file_path)
        
        assert len(questions) == 1
        assert questions[0].text == "¿Cuál es la capital de Francia?"
        assert questions[0].answer == "B"
        assert len(questions[0].options) == 3
    
    def test_parse_multiple_questions(self):
        """Test parsing de múltiples preguntas."""
        content = """¿Cuál es la capital de Francia?
A) Londres
B) París
C) Madrid
ANSWER: B

¿Cuántos días tiene una semana?
A) 5
B) 6
C) 7
ANSWER: C"""
        
        file_path = self.create_temp_file(content)
        questions = self.parser.parse_file(file_path)
        
        assert len(questions) == 2
    
    def test_parse_multiline_question(self):
        """Test parsing de pregunta con múltiples líneas."""
        content = """Esta es una pregunta
que tiene múltiples líneas
¿Cuál es la respuesta?
A) Opción 1
B) Opción 2
ANSWER: A"""
        
        file_path = self.create_temp_file(content)
        questions = self.parser.parse_file(file_path)
        
        assert len(questions) == 1
        assert "múltiples líneas" in questions[0].text
    
    def test_parse_file_not_found(self):
        """Test archivo no encontrado."""
        with pytest.raises(FileNotFoundError):
            self.parser.parse_file(Path("nonexistent.txt"))
    
    def test_parse_incomplete_question(self):
        """Test pregunta incompleta (sin ANSWER)."""
        content = """¿Pregunta sin respuesta?
A) Opción 1
B) Opción 2"""
        
        file_path = self.create_temp_file(content)
        questions = self.parser.parse_file(file_path)
        
        assert len(questions) == 0


class TestQTIGenerator:
    """Tests para el generador QTI."""
    
    def setup_method(self):
        """Configuración para cada test."""
        self.generator = QTIGenerator()
        self.sample_question = Question(
            text="¿Test question?",
            options={"A": "Option 1", "B": "Option 2"},
            answer="A"
        )
    
    def test_generate_item_xml(self):
        """Test generación de XML de pregunta."""
        xml_content = self.generator.generate_item_xml(
            self.sample_question, 
            "test_id"
        )
        
        assert "assessmentItem" in xml_content
        assert "test_id" in xml_content
        assert "Option 1" in xml_content
        assert "Option 2" in xml_content
    
    def test_generate_valid_xml(self):
        """Test que el XML generado sea válido."""
        xml_content = self.generator.generate_item_xml(
            self.sample_question,
            "test_id"
        )
        
        # Verificar que se puede parsear
        try:
            ET.fromstring(xml_content)
        except ET.ParseError:
            pytest.fail("XML generado no es válido")
    
    def test_generate_manifest(self):
        """Test generación de manifest."""
        resources = [("id1", "file1.xml"), ("id2", "file2.xml")]
        manifest_content = self.generator.generate_manifest(resources)
        
        assert "manifest" in manifest_content
        assert "file1.xml" in manifest_content
        assert "file2.xml" in manifest_content
    
    def test_safe_title(self):
        """Test generación de títulos seguros."""
        long_text = "a" * 100
        safe_title = self.generator._safe_title(long_text, 50)
        
        assert len(safe_title) <= 53  # 50 + "..."
        assert safe_title.endswith("...")


class TestPackageBuilder:
    """Tests para el constructor de paquetes."""
    
    def setup_method(self):
        """Configuración para cada test."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.builder = PackageBuilder(self.temp_dir)
        self.sample_questions = [
            Question(
                text="Question 1",
                options={"A": "Opt 1", "B": "Opt 2"},
                answer="A"
            ),
            Question(
                text="Question 2", 
                options={"A": "Opt A", "B": "Opt B"},
                answer="B"
            )
        ]
    
    def test_build_package(self):
        """Test construcción completa del paquete."""
        output_path = self.builder.build_package(
            self.sample_questions,
            "test_package"
        )
        
        assert output_path.exists()
        assert output_path.suffix == ".zip"
        
        # Verificar contenido del ZIP
        with zipfile.ZipFile(output_path, 'r') as zipf:
            files = zipf.namelist()
            assert "imsmanifest.xml" in files
            # Verificar que hay archivos de preguntas
            question_files = [f for f in files if f.startswith("question_")]
            assert len(question_files) == 2


# Tests de integración
class TestIntegration:
    """Tests de integración completa."""
    
    def setup_method(self):
        """Configuración para tests de integración."""
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def test_full_workflow(self):
        """Test del flujo completo Aiken -> QTI."""
        # Crear archivo Aiken
        aiken_content = """¿Cuál es 2+2?
A) 3
B) 4  
C) 5
ANSWER: B

¿Capital de España?
A) Madrid
B) Barcelona
ANSWER: A"""
        
        aiken_file = self.temp_dir / "test.txt"
        with open(aiken_file, 'w', encoding='utf-8') as f:
            f.write(aiken_content)
        
        # Parsear
        parser = AikenParser()
        questions = parser.parse_file(aiken_file)
        
        # Construir paquete
        builder = PackageBuilder(self.temp_dir)
        output_path = builder.build_package(questions, "integration_test")
        
        # Verificaciones
        assert output_path.exists()
        assert len(questions) == 2
        
        # Verificar contenido del ZIP
        with zipfile.ZipFile(output_path, 'r') as zipf:
            files = zipf.namelist()
            assert "imsmanifest.xml" in files
            
            # Verificar manifest
            manifest_content = zipf.read("imsmanifest.xml").decode('utf-8')
            assert "manifest" in manifest_content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])