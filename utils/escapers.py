import html

def latex_escape(text):
    # 17/08/2026. This function escapes out problematic characters in LaTeX.
    replacements = {
        "&": "\\&",
        "%": "\\%",
        "$": "\\$",
        "#": "\\#",
        "_": "\\_"
    }
    for k,v in replacements.items():
        text = text.replace(k,v)
    return text

def html_escape_quotes(text):
    escaped = html.escape(text, quote=False)
    escaped = escaped.replace("'", "&apos;")
    escaped = escaped.replace('"', "&quot;")
    return escaped
