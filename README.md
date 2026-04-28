# Language Reference Sheet Generator

## Overview

A Python-based tool for generating language reference sheets from a structured SQLite database.

The program queries stored vocabulary and produces formatted output in multiple formats, including plain text, HTML, and LaTeX. It is designed to minimise manual formatting work by automating the transformation from raw data to readable reference material.

---

## Features

* Structured vocabulary storage using SQLite
* Supports multiple languages:

  * German (DE)
  * Spanish (ES)
  * French (FR)
  * Italian (IT)
* Supports multiple word types:

  * Nouns
  * Verbs
  * Adjectives
* Generates formatted reference sheets in:

  * Plain text
  * HTML
  * LaTeX
  * PDF
  * CSV
  * Console output
* Language-aware formatting (e.g. handling grammatical gender and adjective forms)

---

## Tech Stack

* Python 3
* SQLite
* HTML (for web output)
* LaTeX (for typeset documents)
* pdflatex (for PDF export)

---

## How It Works

1. The user selects:

   * A language (e.g. DE, ES, FR, IT)
   * A word type (noun, verb, adjective)

2. The program:

   * Queries the SQLite database using parameterised SQL
   * Retrieves relevant rows and column metadata

3. The data is:

   * Formatted according to the selected output type
   * Written to file(s) and/or displayed in the console

---

## Setup

### Requirements

* MiKTeX
* Python 3.x

### Steps

1. Clone the repository
2. Install MiKTeX if not already installed.
3. Ensure the database file is in place:

```
database/flubb.db
```

4. Run the program:

```
python main.py
```

5. Follow the prompts to select:

   * Language
   * Word type
   * Output format(s)

---

## Output

Generated files are written to:

```
output/
```

Depending on selection, outputs may include:

* `.txt` — plain text tables
* `.html` — structured HTML documents
* `.tex` — LaTeX source files
* `.pdf` — Portable Document Files
* `.csv` — Comma Separated Values

---

## Project Structure

```
database/
    flubb.db

exporters/
	(functions for exportation to different file formats)
	
formatters/
	(functions for the formatting of text for various formats)

output/
    (generated files)

utils/
	(functions to change field names to something more meaningful, and escape out problematic characters)

database.py
main.py

```

---

## Example Use Case

Generate a German noun reference sheet:

* Input:
  Language → DE
  Word type → noun

* Output:
  Table including:

  * English translation
  * German lemma
  * Grammatical gender

---

## Status

Core functionality is complete:

* Database schema established
* Query system implemented
* Multi-format export working

---

## Future Improvements

* GUI or web interface
* Expanded dataset
* Enhanced HTML styling
* Additional export formats
* Improved document layout for LaTeX output

---

## Notes

This project focuses on:

* Data modelling
* Query design
* Automated document generation

LibreOffice integration was explored early on but is not part of the current workflow.
