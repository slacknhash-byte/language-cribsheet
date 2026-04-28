# This file contains functions for the formatting of output as
# a table in LaTeX format (.tex)

from utils.headers import clean_heading, get_language
from utils.escapers import latex_escape

def format_latex(row, col_widths=None, column_langs=None, is_header=False, lang=None):
    if is_header:
        return " & ".join(
            f"\\textbf{{{clean_heading(col, lang).capitalize()}}}"
            for col in row
        ) + " \\\\"
    else:
        return " & ".join(latex_escape(str(v)) for v in row) + " \\\\"
