# Refactored 27/04/2026 to allow easier addition of more output formats.
# Updated 28/04/2026: CSV format export.

import os
from database import run_query, generate_query
from pathlib import Path

from formatters.latex_formatters import format_latex
from formatters.html_formatters import format_html
from exporters.text_exporters import export_text_file
from exporters.html_exporters import export_html_file
from exporters.latex_exporters import export_latex_file
from exporters.pdf_exporters import export_pdf
from exporters.screen_exporters import output_to_screen
from exporters.csv_exporters import export_csv_file
#####

def get_values():
    # 05/03/26 Added validation for language and word type.
    valid_langs = ['DE','ES','FR','IT']
    valid_types = ['noun','verb','adjective']
    while True:
        print("Select a language:")
        print("DE\tGerman\r\nES\tSpanish\r\nFR\tFrench\r\nIT\tItalian\r\n")
        word_language = input().upper()
        if word_language in valid_langs:
            break
    print("Select a word type:")
    while True:
        print("\tNoun\r\n\tVerb\r\n\tAdjective")
        word_type = input().lower()
        if word_type in valid_types:
            break
    return word_language, word_type
    

def get_output_type(cols, rows, word_language, word_type):
    print("What format of reference sheet do you want?\n")

    options = [
        ("Plain text", export_text_file),
        ("Comma-Separated Values (CSV)", export_csv_file),
        ("PDF", export_pdf),
        ("LaTeX", export_latex_file),
        ("HTML", export_html_file),
        ("Output to the screen", output_to_screen),
    ]

    def ask_yes_no(prompt):
        while True:
            answer = input(f"{prompt}? ").strip().lower()
            if answer in ("y", "yes"):
                return True
            if answer in ("n", "no"):
                return False

    for label, func in options:
        if ask_yes_no(label):
            func(cols, rows, word_language, word_type)

#####
            
if __name__ == "__main__":
    word_language, word_type = get_values()
    rows, cols = run_query(word_language,word_type)
    get_output_type(cols, rows, word_language, word_type)
