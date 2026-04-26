from utils.headers import clean_heading, get_language

def format_text(row, col_widths=None, column_langs=None, is_header=False, lang=None):
    if is_header:
        row = [
            clean_heading(str(col), lang).capitalize()
            for col in row
        ]
    else:
        row = [str(v) for v in row]

    return " | ".join(
        row[i].ljust(col_widths[i]) for i in range(len(row))
    )
