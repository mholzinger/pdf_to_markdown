# PDF to Markdown Converter

## Overview

This project provides a tool to convert PDF files into Markdown format, with a focus on optimizing the input for Large Language Models (LLMs). The main goal is to prevent unnecessary token consumption when feeding PDF files to LLM agents, especially those that treat PDF pages as images, which can be highly inefficient and costly.

## Motivation

Many LLM-based applications process PDF files by converting each page into an image, resulting in excessive token usage and increased costs. This project addresses this issue by extracting the textual content from PDFs and converting it into clean, structured Markdown. This approach ensures that only meaningful text is sent to the LLM, significantly reducing token usage and improving processing efficiency.

## Features

- Extracts text from PDF files and converts it to Markdown
- Preserves document structure (headings, paragraphs, lists, etc.) where possible
- Reduces token usage by avoiding image-based PDF processing
- Simple command-line interface for ease of use

## Usage

1. Place your PDF file in the project directory.
2. Run the main script to convert the PDF to Markdown:

   ```bash
   python main.py input.pdf output.md
   ```

   Replace `input.pdf` with the name of your PDF file and `output.md` with the desired output Markdown file name.

## Requirements

- Python 3.7+
- [pdfminer.six](https://github.com/pdfminer/pdfminer.six) or similar library for PDF text extraction

Install dependencies with:

```bash
pip install pdfminer.six
```

## Example

Given a PDF file `sample.pdf`, convert it to Markdown:

```bash
python main.py sample.pdf sample.md
```

## Why Not Images?

LLMs process text more efficiently than images. When PDFs are treated as images, every page is converted to a large block of tokens, quickly exhausting token limits and increasing costs. By extracting and structuring the text, this tool ensures that only the relevant content is processed, making LLM-based workflows more scalable and affordable.

## License

MIT License

## Contributing

Contributions are welcome! Please open issues or submit pull requests to help improve this project.
