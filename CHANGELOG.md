# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2025-11-26

### Added
- Complete rewrite with object-oriented architecture
- New `Question`, `AikenParser`, `QTIGenerator`, and `PackageBuilder` classes
- Comprehensive error handling and validation
- Configurable logging system with multiple levels
- Type hints throughout the codebase
- Complete unit test suite with pytest
- Development tools integration (Black, flake8, mypy)
- Automated setup script (`setup.py`)
- Development automation script (`dev.py`)
- GitHub Actions CI/CD pipeline
- Support for multiple Python versions (3.7-3.11)
- Professional project structure with documentation
- Virtual environment activation scripts for Windows

### Enhanced
- Better Aiken format parsing with multiline question support
- Improved QTI 2.1 XML generation with validation
- More robust file encoding detection (UTF-8 and Latin-1)
- Enhanced command-line interface with more options
- Better error messages and user feedback

### New Features
- `--create-sample` flag to generate example files
- `--validate-only` flag to check files without conversion
- `--verbose` flag for detailed logging
- Automatic cleanup of temporary files
- Response processing templates in QTI XML
- Improved manifest generation with metadata

### Documentation
- Comprehensive README with installation and usage examples
- Contributing guidelines (`CONTRIBUTING.md`)
- Code of conduct (`CODE_OF_CONDUCT.md`)
- Professional license (MIT)
- Setup guide for GitHub deployment

### Development
- Complete test coverage with integration tests
- Automated code formatting and linting
- Type checking with mypy
- Development environment automation
- GitHub Actions workflow for continuous integration

## [1.0.0] - 2025-11-25

### Added
- Initial version of Aiken to QTI converter
- Basic Aiken format parsing
- QTI 2.1 XML generation
- ZIP package creation for LMS import
- Support for multiple choice questions
- Command-line interface

### Features
- Convert Aiken format text files to QTI 2.1 packages
- Generate IMS manifest for LMS compatibility
- Support for Canvas, Blackboard, Moodle, and other LMS platforms
- Unique identifiers to prevent conflicts