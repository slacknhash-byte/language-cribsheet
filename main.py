import sqlite3
import html
import subprocess
import os
from pathlib import Path

def write_rows(rows, formatter, output=None):
    # 17/03/2026
    # This function outputs the rows of the table.
    # The formatter argument points at one of the format_row_ functions.
    # 21/03/26 output is nor optional, allowing write_rows to be used in output_to_screen()
    for row in rows:
        if output is not None:
            output.write(formatter(row) + "\n")
        else:
            print(formatter(row) + "\n")

# formatters

def format_header_row_text(columns):
    # 20/03/2026
    # This function determines how column titles are tabulated in the plain text version of the document
    return "\t".join(str(col.replace('_',' ').capitalize()) for col in columns)

def format_row_text(row):
    # 17/03/2026
    # This function determines how items are tabulated in the plain text version of the document
    return "\t".join(str(v) for v in row)

def format_header_row_latex(columns):
    # 21/03/2026
    # This function determines how column titles are tabulated in the
    # LaTeX version of the document
   
    return " & ".join(f"\\textbf{{{col.replace('_',' ').capitalize()}}}" for col in columns) + " \\\\\n"

def format_row_latex(row):
    # 17/03/2026
    # This function determines how items are tabulated in the
    # LaTeX version of the document
    return " & ".join(latex_escape(str(v)) for v in row) + " \\\\"

def format_header_row_html(columns):
    # 19/03/2026
    # This function determines how items are tabulated in the
    # HTML version of the document
    return "\t<tr>" + "".join(f"<th scope=\"col\">{col.replace('_',' ').capitalize()}</th>" for col in columns) + "</tr>"

def format_row_html(row, column_langs):
    # 19/03/2026
    # Updated 24/03/2026 to add language coding
    # This function determines how items are tabulated in the
    # HTML version of the document
    return "\t<tr>" + "".join(
        f'<td lang="{lang}">{html_escape_named(str(v))}</td>'
        for v, lang in zip(row, column_langs)
    ) + "</tr>"

def format_header_row_screen(columns):
    # 20/03/2026
    # This function determines how column titles are tabulated in the on-screen
    # display
    return "\t".join(str(col.replace('_',' ').capitalize()) for col in columns) + "\n"

def format_row_screen(row):
    # 17/03/2026
    # This function determines how items are tabulated in the on-screen display
    return "\t".join(str(v) for v in row)

# LaTeX-exclusive functions

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

def latex_preamble(f):
    # 18/03/2026. Added function to generate preamble for LaTeX file to reduce size of export_latex_file()
    # 15/04/2026. Removed instruction to include fontenc as it doesn't work with pdflatex.
    f.write("\\documentclass[a4paper,oneside]{slides}\n")
    f.write("\\usepackage[utf8]{inputenc}\n")
    f.write("\\usepackage[T1]{fontenc}\n")

def latex_top_matter(f):
    #18/03/2026. This function prints the top matter for the LaTeX file.
    f.write("\\title{Flubb's Reference}\n")
    f.write("\\author{Phil Smith}\n")
    f.write("\\date{March 2026}\n")
    f.write("\\maketitle\n")

def latex_format_columns(word_type,word_language):
    # 03/03/2026 This function returns a string of instructions indicating the
    # number and alignment of the table's columns in the LaTeX document. German has more
    # genders than other European languages -- neuter, and plural -- and so its table
    # of adjectives is more extensive.
    column_formats = {
        "noun": "{l r r}",
        "verb": "{l r}"
    }
    if word_type == "adjective":
       column_string = "{l r r r r r}" if word_language == "DE" else "{l r r r}"
    else:
        column_string = column_formats[word_type]
    return column_string + "\n";

# HTML-exclusive functions

def build_column_langs(word_language, word_type, row_length):
    langs = ["en"]

    if word_type == "noun":
        langs += [word_language.lower()] * (row_length - 2)
        langs.append("en")
    else:
        langs += [word_language.lower()] * (row_length - 1)

    return langs

def html_escape_named(text):
    escaped = html.escape(text, quote=False)
    escaped = escaped.replace("'", "&apos;")
    escaped = escaped.replace('"', "&quot;")
    return escaped

def get_language(code):
    language_dict = {
        "DE": "German",
        "ES": "Spanish",
        "FR": "French",
        "IT": "Italian"
    }
    return language_dict[code]

def html_header(f, word_language, word_type):
    # 20/03/2026 This function outputs the <head> element and its contents
    # for the HTML file.

    f.write("<head>\n")
    f.write("\t<meta charset=\"utf-8\">\n")
    f.write(f"\t<meta name=\"description\" content=\"A reference sheet containing {get_language(word_language)} {word_type}s\">\n")
    f.write(f"\t<title>Language Reference Sheet: {get_language(word_language)} {word_type}s</title>\n")
    f.write("</head>\n")

def html_body(f, word_language, word_type, cols, rows):
    # 20/03/2026 This function outputs the <body> element and its contents
    # for the HTML file
    f.write("<body>\n")
    f.write("<header></header>\n")
    f.write("<nav></nav>\n")
    f.write("<main>\n")
    f.write(f"<table id=\"{word_language}_{word_type}\">\n")
    f.write(f"\t<caption>{get_language(word_language)} {word_type.capitalize()}s</caption>\n")    
    f.write("\t<thead>\n")
    column_langs = build_column_langs(word_language, word_type, len(cols))    
    f.write(format_header_row_html(cols))
    f.write("\n\t</thead>\n\t<tbody>\n")
    write_rows(rows, lambda r: format_row_html(r, column_langs), f)
    f.write("\n\t</tbody>\n\t<tfoot>\n\t<tr></tr>\n\t</tfoot>\n")
    f.write("</table>\n")
    f.write("</main>\n")
    f.write("<footer></footer>\n")
    f.write("</body>\n")

# File exportation functions

def export_latex_file(cols, rows, word_language, word_type):
    # 03/03/2026 This function takes the data that has been read into the
    # cursor variable and outputs it to a LaTeX file.
    # 18/03/2026 Spun off latex_preamble() and latex_top_matter()
    # 19/03/2026 File output is based on the language and type of word.
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    file_name = f"{word_language}_{word_type}.tex"
    file_path = output_dir / file_name
    with open(file_path,"w",encoding="utf-8-sig") as f:
        latex_preamble(f)
        f.write("\\begin{document}\n") # keep \begin and \end on same line       
        latex_top_matter(f)
        # 18/03/2026 As the LaTeX file's features develop,
        # I may have to spin off everything between \begin{tabular} and \end{tabular}
        # into another function: populate_table(word_language, word_type, rows, f)
        f.write("  \\begin{tabular}")
        f.write(latex_format_columns(word_type,word_language))
        f.write(format_header_row_latex(cols))
        write_rows(rows, format_row_latex, f)
        f.write("  \\end{tabular}\n")
        # Stuff at the foot of the document, again, maybe another function...
        f.write("\\end{document}\n")

def export_pdf(cols, rows, word_language, word_type):
    # 16/04/2026 This function looks for a LaTeX file, and converts it to a PDF.
    # If the LaTeX file is not present, the function calls export_latex_file()
    # and uses the arguments to generate such a file from a database query.
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    file_name = f"{word_language}_{word_type}"
    file_path = output_dir / file_name

    tex_file = file_path.with_suffix(".tex")

    # Ensure .tex exists
    if not tex_file.exists():
        export_latex_file(cols, rows, word_language, word_type)

    # Run pdflatex twice
    for _ in range(2):
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_file.name],
            cwd=output_dir,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print("LaTeX compilation failed:")
            print(result.stdout)
            return False

    # Clean up auxiliary files
    for ext in [".log", ".aux"]:
        aux_file = file_path.with_suffix(ext)
        try:
            aux_file.unlink()
        except FileNotFoundError:
            pass

    return True
    
def export_html_file(cols, rows, word_language, word_type):
    # 20/03/2026 This finction takes the data that has been read into the
    # cursor variable and outputs it to an HTML document.
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    file_name = f"{word_language}_{word_type}.html"
    file_path = output_dir / file_name
    with open(file_path,"w",encoding="utf-8-sig") as f:
        f.write("<!doctype html>\n")
        f.write("<html lang=\"en\">\n")
        html_header(f, word_language, word_type)
        html_body(f, word_language, word_type, cols, rows)
        f.write("</html>\n")
               
def export_text_file(cols, rows, word_language, word_type):
    # 02/03/2026 This function takes the data that has been read into the
    # cursor variable and outputs it to a text file, inserting a tab between each
    # field and a carriage return and newline after each record.
    # Updated 18/03/2026. Removed loop, added write_rows() call.
    # 19/03/2026 File output is based on the language and type of word.
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)    
    file_name = f"{word_language}_{word_type}.txt"
    file_path = output_dir / file_name
    with open(file_path,"w",encoding="utf-8-sig") as f:
        # Column headers
        f.write(format_header_row_text(cols).upper())
        f.write("\n")
        #tabular data
        write_rows(rows, format_row_text, f)

def output_to_screen(cols, rows, word_language, word_type):
    # 02/03/2026 This function takes the data that has been read into the
    # cursor variable and outputs it to the screen, inserting a tab between each
    # field and a carriage return and newline after each record.
    # Updated 21/03/2026. Removed loop, added write_rows() call.
    
    # Column headers
    f = None # No filehandling involved in this function.
    print(format_header_row_screen(cols))
    write_rows(rows, format_row_screen, f)

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
    
def run_query(word_language, word_type):
    # Last modified 22/03/26
    # This function connects to flubb.db, generates a query, and
    # returns a 2-dimensional array containing the row data and
    # a list containing the column names.
    
    with sqlite3.connect('database/flubb.db') as conn:
        cursor = conn.cursor()
        query, params = generate_query(word_language, word_type)
        cursor.execute(query, params)
        rows = cursor.fetchall()
        cols = [desc[0] for desc in cursor.description]
        return rows, cols

def get_output_type(cols, rows, word_language, word_type):
    print("What format of reference sheet do you want?\n")

    options = [
        ("Plain text", export_text_file),
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

def generate_query(word_language, word_type):
    query_string = "SELECT mw.english, mw.lemma"
    if word_type == "noun":
        query_string += ", g.gender_name"       
    if word_type == "adjective":
        query_string += ", mw.masculine_form, mw.feminine_form"
        if word_language == "DE":
            query_string += ", mw.neuter_form, mw.plural_form"           
    query_string += " FROM master_words mw"
    query_string += " JOIN word_classes wc ON mw.word_class_id = wc.id"
    query_string += " JOIN languages l ON mw.language_id = l.id"  
    if word_type == "noun":
        query_string += " LEFT JOIN genders g ON mw.gender_id = g.id"      
    query_string += " WHERE wc.class_name = ? AND l.code = ?"   
    return query_string, (word_type, word_language)

if __name__ == "__main__":
    word_language, word_type = get_values()
    rows, cols = run_query(word_language,word_type)
    get_output_type(cols, rows, word_language, word_type)
