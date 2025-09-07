# AnnotatorX

An end-to-end data annotation pipeline that ensures reproducibility, validation, and automation. AnnotatorX provides a CLI for managing datasets, applying annotations, validating them against deterministic test cases, and running everything inside Docker for isolation.

## Features

- **CLI Tool** with subcommands for dataset ingestion, annotation, validation, export, and statistics
- **Deterministic Annotations** with seed-based reproducibility
- **Schema Validation** using Pydantic for robust data validation
- **Docker Integration** for reproducible runs across environments
- **CI/CD Pipeline** with GitHub Actions for automated validation
- **Comprehensive Testing** with pytest for deterministic validation

## Quick Start

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd annotate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the CLI:
```bash
python -m annotatorx --help
```

### Basic Usage

1. **Ingest a dataset:**
```bash
python -m annotatorx ingest datasets/example_dataset.csv
```

2. **Annotate the dataset:**
```bash
python -m annotatorx annotate example_dataset --seed 0
```

3. **Validate annotations:**
```bash
python -m annotatorx validate annotations/annotations.json
```

4. **Export to CSV:**
```bash
python -m annotatorx export annotations/annotations.json --format csv
```

5. **View statistics:**
```bash
python -m annotatorx stats annotations/annotations.json
```

## Docker Usage

### Build and run with Docker:
```bash
docker build -t annotatorx .
docker run --rm -v $(pwd)/datasets:/app/datasets -v $(pwd)/annotations:/app/annotations annotatorx python -m annotatorx --help
```

### Using docker-compose:
```bash
# Run tests
docker-compose run --rm test

# Validate example annotations
docker-compose run --rm validate

# Run CLI commands
docker-compose run --rm annotatorx python -m annotatorx annotate example_dataset
```

## CLI Commands

### `ingest <file>`
Import a dataset (CSV/JSON) into the datasets directory.

**Options:**
- `--name`: Optional dataset name to store as
- `--format`: Specify format if ambiguous (csv/json)

**Example:**
```bash
python -m annotatorx ingest data.csv --name my_dataset
```

### `annotate <dataset>`
Apply annotation functions to a dataset and write JSON annotations.

**Options:**
- `--output`: Output file path (default: annotations/annotations.json)
- `--label-field`: Annotation label field name (default: label)
- `--text-field`: Input text field name (default: text)
- `--seed`: Seed for deterministic behavior (default: 0)
- `--limit`: Limit number of rows to process

**Example:**
```bash
python -m annotatorx annotate my_dataset --seed 42 --limit 100
```

### `validate <annotations>`
Validate annotation JSON against schema using Pydantic.

**Example:**
```bash
python -m annotatorx validate annotations/annotations.json
```

### `export <annotations>`
Export annotations to CSV or JSON format.

**Options:**
- `--format`: Output format (csv/json, default: csv)
- `--output`: Output file path

**Example:**
```bash
python -m annotatorx export annotations/annotations.json --format csv --output results.csv
```

### `stats <annotations>`
Show summary metrics for annotations including label distribution.

**Example:**
```bash
python -m annotatorx stats annotations/annotations.json
```

## Project Structure

```
annotate/
├── annotatorx/                 # Core Python CLI package
│   ├── __main__.py            # CLI entrypoint
│   ├── pipeline/              # Annotation pipeline modules
│   │   └── annotate.py        # Annotation logic
│   ├── validators/            # Schema validation
│   │   └── schemas.py         # Pydantic schemas
│   └── utils/                 # Utilities
│       └── io.py              # File I/O operations
├── datasets/                  # Input datasets (CSV/JSON)
│   ├── example_dataset.csv
│   └── example_dataset.json
├── annotations/               # Annotation outputs (JSON)
│   └── example_annotations.json
├── tests/                     # Test cases
│   ├── test_pipeline.py
│   ├── test_validation.py
│   └── test_io.py
├── docker/                    # Docker configuration
│   ├── Dockerfile
│   └── docker-compose.yml
├── .github/workflows/         # CI/CD pipelines
│   └── ci.yml
├── docs/                      # Documentation
│   ├── schemas.md
│   └── examples.md
├── requirements.txt
├── .gitignore
├── .dockerignore
└── README.md
```

## Development

### Running Tests
```bash
python -m pytest tests/ -v
```

### Running with Coverage
```bash
python -m pytest tests/ --cov=annotatorx --cov-report=html
```

### Linting
```bash
# Add linting tools to requirements.txt as needed
python -m flake8 annotatorx/
python -m black annotatorx/
```

## CI/CD

The project includes GitHub Actions workflows that:
- Run tests on every push and pull request
- Validate example annotations
- Test Docker container builds
- Run docker-compose validation

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## Support

For issues and questions, please open an issue on the GitHub repository.
