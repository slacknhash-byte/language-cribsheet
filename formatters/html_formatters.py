# This file contains functions for the formatting of output as
# table cells in HTML format

from utils.headers import clean_heading, get_language
from utils.escapers import html_escape_quotes

def format_html(row, col_widths=None, column_langs=None, is_header=False, lang=None):
    if is_header:
        return "<thead>\n\t<tr>" + "".join(
            f"<th scope=\"col\">{clean_heading(col, lang).capitalize()}</th>"
            for col in row
        ) + "</tr>\n\t</thead>\n\t<tbody>\n"
    else:
        return "\t<tr>" + "".join(
            f'<td lang="{lang_code}">{html_escape_quotes(str(v))}</td>'
            for v, lang_code in zip(row, column_langs)
        ) + "</tr>"
    
