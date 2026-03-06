
# PDF to Markdown Converter

## Overview

This project is designed for enterprise environments, supporting multi-host deployments and importable as a Python package. It converts PDF files to Markdown, optimizing input for LLMs and reducing token usage by avoiding image-based PDF processing.

## Features

- Enterprise-ready, importable Python package
- Multi-host and scalable architecture
- Extracts and converts PDF text to Markdown
- Reduces token usage for LLMs
- Command-line and API usage

## Installation

Install via pip (after packaging):

```bash
pip install pdf_to_markdown
```

Or clone and install locally:

```bash
pip install .
```

## Usage

### As a Python Package

```python
from pdf_to_markdown.converter import PDFToMarkdownConverter

converter = PDFToMarkdownConverter(output_dir="/path/to/output")
markdown = converter.convert("input.pdf", "output.md")
```

### Command Line

```bash
python main.py input.pdf output.md
```

## Requirements

- Python 3.7+
- pdfminer.six

## Enterprise & Multi-Host Support

- Designed for integration with distributed systems
- Can be deployed across multiple hosts
- Suitable for batch processing and automation

## License

MIT License

## Contributing

Contributions are welcome! Please open issues or submit pull requests.
