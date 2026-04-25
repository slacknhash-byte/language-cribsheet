import sqlite3
import html
import subprocess
import os
from pathlib import Path



##########################################################################

##
#Database functions

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

##
#Utils
#
#Escaping

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

def html_escape_named(text):
    escaped = html.escape(text, quote=False)
    escaped = escaped.replace("'", "&apos;")
    escaped = escaped.replace('"', "&quot;")
    return escaped

#Headers
def clean_heading(name, lang):
    # 17/04/2026. Some of the field names in the database don't make
    # good column headers on the reference tables. This function provides
    # more fitting substitutes.
    # 18/04/2026. Expanded dictionary.
    
    replacements = {
        'gender_name': 'gender',
        'lemma': get_language(lang),
        'masculine_form': 'masculine',
        'feminine_form': 'feminine',
        'neuter_form': 'neuter',
        'plural_form': 'plural',
        }
    return replacements.get(name,name)

def get_language(code):
    language_dict = {
        "DE": "German",
        "ES": "Spanish",
        "FR": "French",
        "IT": "Italian"
    }
    return language_dict[code]

##
#Formatters
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

def format_html(row, col_widths=None, column_langs=None, is_header=False, lang=None):
    if is_header:
        return "<thead>\n\t<tr>" + "".join(
            f"<th scope=\"col\">{clean_heading(col, lang).capitalize()}</th>"
            for col in row
        ) + "</tr>\n\t</thead>\n\t<tbody>\n"
    else:
        return "\t<tr>" + "".join(
            f'<td lang="{lang_code}">{html_escape_named(str(v))}</td>'
            for v, lang_code in zip(row, column_langs)
        ) + "</tr>"
    
def format_latex(row, col_widths=None, column_langs=None, is_header=False, lang=None):
    if is_header:
        return " & ".join(
            f"\\textbf{{{clean_heading(col, lang).capitalize()}}}"
            for col in row
        ) + " \\\\"
    else:
        return " & ".join(latex_escape(str(v)) for v in row) + " \\\\"


##
#Exporters
def export_text_file(column_headers, data_rows, table_language, word_type):
    # 02/03/2026 This function takes the data that has been read into the
    # cursor variable and outputs it to a text file, inserting a tab between each
    # field and a carriage return and newline after each record.
    # Updated 18/03/2026. Removed loop, added write_rows() call.
    # 19/03/2026 File output is based on the language and type of word.
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)    
    file_name = f"{table_language}_{word_type}.txt"
    file_path = output_dir / file_name
    with open(file_path,"w",encoding="utf-8-sig") as file_output:
     
        #tabular data
        # Column header should go here
        col_count = len(data_rows[0])
        column_widths = [
            max(
                max(len(str(row[i])) for row in data_rows),
                len(str(column_headers[i]))
            )
            for i in range(col_count)
        ]
       
        write_table(data_rows, column_headers, format_text, file_output, column_widths, None, table_language)

def export_html_file(column_headers, data_rows, table_language, word_type):
    # 20/03/2026 This finction takes the data that has been read into the
    # cursor variable and outputs it to an HTML document.
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    file_name = f"{word_language}_{word_type}.html"
    file_path = output_dir / file_name
    with open(file_path,"w",encoding="utf-8-sig") as file_output:
        file_output.write("<!doctype html>\n")
        file_output.write("<html lang=\"en\">\n")
        html_head(file_output, table_language, word_type)
        html_body(file_output, table_language, word_type, column_headers, data_rows)
        file_output.write("</html>\n")

def export_latex_file(column_headers, data_rows, table_language, word_type):
    # 03/03/2026 This function takes the data that has been read into the
    # cursor variable and outputs it to a LaTeX file.
    # 18/03/2026 Spun off latex_preamble() and latex_top_matter()
    # 19/03/2026 File output is based on the language and type of word.
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    file_name = f"{word_language}_{word_type}.tex"
    file_path = output_dir / file_name
    with open(file_path,"w",encoding="utf-8-sig") as file_output:
        latex_preamble(file_output)
        file_output.write("\\begin{document}\n") # keep \begin and \end on same line       
        latex_top_matter(file_output)
        file_output.write("\\begin{longtable}")
        file_output.write(latex_format_columns(word_type, table_language))

        # header (first page)
        header_line = format_latex(
            column_headers,
            is_header=True,
            lang=table_language
        )
        file_output.write(header_line + "\n")
        file_output.write("\\endfirsthead\n")

        # header (subsequent pages)
        file_output.write(header_line + "\n")
        file_output.write("\\endhead\n")

        # actual data
        write_rows_only(
            data_rows,
            format_latex,
            file_output,
            table_language=table_language
        )

        file_output.write("\\end{longtable}\n")
        file_output.write("\\end{document}\n")

def export_pdf(column_headers, data_rows, word_language, word_type):
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
        export_latex_file(column_headers, data_rows, word_language, word_type)

    # Run pdflatex twice
    # THIS WILL HAVE TO CHANGE AS WE'RE NOT USING PDFLATEX ANY MORE
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

##
#Main functions

def write_table(
    data_rows,        # list of tuples returned from database
    column_headers,   # column names from cursor.description
    row_formatter,    # function that formats a single row
    output_stream=None,  # file handle or None for stdout
    column_widths=None,  # widths for fixed-width formats (text/screen)
    cell_languages=None, # per-column language codes (HTML)
    table_language=None  # language for headings/labels
):

    # header
    header_line = row_formatter(
        column_headers,
        column_widths,
        cell_languages,
        is_header=True,
        lang=table_language
    )

    if output_stream:
        output_stream.write(header_line + "\n")
    else:
        print(header_line)

    # rows
    for row in data_rows:
        line = row_formatter(
            row,
            column_widths,
            cell_languages,
            is_header=False,
            lang=table_language
        )

        if output_stream:
            output_stream.write(line + "\n")
        else:
            print(line)

def write_rows_only(
    data_rows,
    row_formatter,
    output_stream=None,
    column_widths=None,
    cell_languages=None,
    table_language=None
):
    for row in data_rows:
        line = row_formatter(
            row,
            col_widths=column_widths,
            column_langs=cell_languages,
            is_header=False,
            lang=table_language
        )
        output_stream.write(line + "\n")            

##
#LaTeX-exclusive functions
def latex_preamble(file_output):
# 18/03/2026. Added function to generate preamble for LaTeX file to reduce size of export_latex_file()
# 15/04/2026. Removed instruction to include fontenc as it doesn't work with pdflatex.
    file_output.write("\\documentclass[a4paper,oneside]{slides}\n")
    file_output.write("\\usepackage{longtable}\n")
    file_output.write("\\usepackage[utf8]{inputenc}\n")
    file_output.write("\\usepackage[T1]{fontenc}\n")
    
# 19/04/2026. The time's come to abandon pdflatex, in order to allow more work with fonts.
#f.write("\\usepackage{fontspec}\n")

def latex_top_matter(file_output):
#18/03/2026. This function prints the top matter for the LaTeX file.
    file_output.write("\\title{Flubb's Reference}\n")
    file_output.write("\\author{Phil Smith}\n")
    file_output.write("\\date{Apr 2026}\n")
    file_output.write("\\maketitle\n")

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

##
#HTML-exclusive functions

def build_cell_languages(word_language, word_type, row_length):
    cell_languages = ["en"]

    if word_type == "noun":
        cell_languages += [word_language.lower()] * (row_length - 2)
        cell_languages.append("en")
    else:
        cell_languages += [word_language.lower()] * (row_length - 1)
    return cell_languages

def html_head(file_output, word_language, word_type):
    # 20/03/2026 This function outputs the <head> element and its contents
    # for the HTML file.

    file_output.write("<head>\n")
    file_output.write("\t<meta charset=\"utf-8\">\n")
    file_output.write(f"\t<meta name=\"description\" content=\"A reference sheet containing {get_language(word_language)} {word_type}s\">\n")
    file_output.write(f"\t<title>Language Reference Sheet: {get_language(word_language)} {word_type}s</title>\n")
    file_output.write("</head>\n")

def html_body(file_output, table_language, word_type, column_headers, data_rows):
    # 20/03/2026 This function outputs the <body> element and its contents
    # for the HTML file
    file_output.write("<body>\n")
    file_output.write("<header></header>\n")
    file_output.write("<nav></nav>\n")
    file_output.write("<main>\n")
    file_output.write(f"<table id=\"{word_language}_{word_type}\">\n")
    file_output.write(f"\t<caption>{get_language(table_language)} {word_type.capitalize()}s</caption>\n")    
    cell_languages = build_cell_languages(table_language, word_type, len(column_headers))    
    write_table(data_rows, column_headers, format_html, file_output, None, cell_languages, table_language)
    file_output.write("\n\t</tbody>\n\t<tfoot>\n\t<tr></tr>\n\t</tfoot>\n")
    file_output.write("</table>\n")
    file_output.write("</main>\n")
    file_output.write("<footer></footer>\n")
    file_output.write("</body>\n")



##

def output_to_screen(column_headers, data_rows, table_language, word_type):
    # 02/03/2026 This function takes the data that has been read into the
    # cursor variable and outputs it to the screen, inserting a tab between each
    # field and a carriage return and newline after each record.
    # Updated 21/03/2026. Removed loop, added write_rows() call.
    
    # Column headers
    f = None # No filehandling involved in this function.
    col_count = len(rows[0])
    column_widths = [
        max(
            max(len(str(row[i])) for row in data_rows),
            len(str(column_headers[i]))
        )
        for i in range(col_count)
    ]    

    write_table(data_rows, column_headers, format_text, None, column_widths, None, table_language)

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
