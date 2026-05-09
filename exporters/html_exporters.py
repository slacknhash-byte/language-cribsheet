from pathlib import Path
from formatters.html_formatters import format_html
from exporters.common_exporters import write_table
from utils.headers import get_language
from utils.titles import document_title, build_codename

def export_html_file(column_headers, data_rows, table_language, word_type):
    # 20/03/2026 This function takes the data that has been read into the
    # cursor variable and outputs it to an HTML document.
    # 09/05/2026 Added create_stylesheet()
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    file_name = f"{table_language}_{word_type}.html"
    file_path = output_dir / file_name
    with open(file_path,"w",encoding="utf-8-sig") as file_output:
        file_output.write("<!doctype html>\n")
        file_output.write("<html lang=\"en\">\n")
        html_head(file_output, table_language, word_type)
        html_body(file_output, table_language, word_type, column_headers, data_rows)
        file_output.write("</html>\n")
    create_stylesheet()

def create_stylesheet():
    # 09/05/2026 This function creates a stylesheet for the HTML export.

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    file_name = "style.css"
    file_path = output_dir / file_name
    css_instructions="""/* Flubb's Reference Sheet stylesheet v0.1 
/* Created 09/05/2025
/* Please keep this file in the same directory as any HTML reference sheets
/* you create. */
body {
    font-family: Georgia, serif;
    color: #222222;
    background: #fafaf8;
    line-height: 1.5;
    margin: 2rem;
}

h1, h2, h3, th {
    font-family: Inter, sans-serif;
}

table {
    border-collapse: collapse;
    width: 100%;
}

th {
    text-align: left;
    border-bottom: 2px solid #cccccc;
    padding: 0.4rem;
}

td {
    padding: 0.3rem 0.4rem;
}

.footer-code {
    font-family: Inter, sans-serif;
    font-size: 0.8rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}"""        

    with open(file_path,"w",encoding="utf-8-sig") as file_output:
        file_output.write(css_instructions)
    
    
def html_head(file_output, table_language, word_type):
    # 20/03/2026 This function outputs the <head> element and its contents
    # for the HTML file.
    # Updated 09/05/2026 to add stylesheet and font references.

    file_output.write("<head>\n")
    file_output.write("\t<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">\n")
    file_output.write("\t<link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>\n")
    file_output.write("\t<link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap\" rel=\"stylesheet\">\n")
    file_output.write("\t<link rel=\"stylesheet\" href=\"style.css\">\n")
    file_output.write("\t<meta charset=\"utf-8\">\n")
    file_output.write(f"\t<meta name=\"description\" content=\"A reference sheet containing {get_language(table_language)} {word_type}s\">\n")
    file_output.write(f"\t<title>Language Reference Sheet: {get_language(table_language)} {word_type}s</title>\n")
    file_output.write("</head>\n")

def html_body(file_output, table_language, word_type, column_headers, data_rows):
    # 20/03/2026 This function outputs the <body> element and its contents
    # for the HTML file
    # 25/04/2026 Updated to include table_write()
    # 30/04/2025 Updated to include build_codename()
    file_output.write("<body>\n")
    file_output.write("<header></header>\n")
    file_output.write("<nav></nav>\n")
    file_output.write("<main>\n")
    file_output.write(f"<h1>{document_title(table_language, word_type)}</h1>\n")
    file_output.write(f"<table id=\"{table_language}_{word_type}\">\n")
    file_output.write(f"\t<caption>{get_language(table_language)} {word_type.capitalize()}s</caption>\n")    
    cell_languages = build_cell_languages(table_language, word_type, len(column_headers))    
    write_table(data_rows, column_headers, format_html, file_output, None, cell_languages, table_language)
    file_output.write("\n\t</tbody>\n\t<tfoot>\n\t<tr></tr>\n\t</tfoot>\n")
    file_output.write("</table>\n")
    file_output.write("</main>\n")
    file_output.write("<footer>\n\t<p class=\"codename\">")
    file_output.write(f"Reference Number: {build_codename(table_language,word_type)}")
    file_output.write("</p>\n</footer>\n")
    file_output.write("</body>\n")

def build_cell_languages(table_language, word_type, row_length):
    cell_languages = ["en"]

    if word_type == "noun":
        cell_languages += [table_language.lower()] * (row_length - 2)
        cell_languages.append("en")
    else:
        cell_languages += [table_language.lower()] * (row_length - 1)
    return cell_languages
