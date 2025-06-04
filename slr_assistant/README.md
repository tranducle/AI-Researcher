# SLR Assistant

This module provides a lightweight command-line interface for conducting systematic literature reviews (SLRs) following the PRISMA protocol. It offers basic project management, PDF handling and integration with large language models.

## Features

- Initialize projects and store study metadata in a local SQLite database.
- Import study records from CSV files.
- Attach and store PDF documents for each study.
- Extract text from PDFs using `pdfminer.six`.
- Ask questions about included study abstracts via an LLM (OpenAI by default).
- Generate a simple PRISMA flow diagram summarizing study counts.

## Usage

```
python -m slr_assistant.cli init my_project
python -m slr_assistant.cli import-records my_project studies.csv
python -m slr_assistant.cli add-pdf my_project 1 path/to/file.pdf
python -m slr_assistant.cli ask my_project "What methodologies are common?" --api_key YOUR_KEY
python -m slr_assistant.cli prisma my_project prisma.png
```

This is a minimal foundation intended for further development.
