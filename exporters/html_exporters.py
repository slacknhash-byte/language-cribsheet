from pathlib import Path
from formatters.html_formatters import format_html
from exporters.common_exporters import write_table
from utils.headers import get_language

def export_html_file(column_headers, data_rows, table_language, word_type):
    # 20/03/2026 This finction takes the data that has been read into the
    # cursor variable and outputs it to an HTML document.
    
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

def html_head(file_output, table_language, word_type):
    # 20/03/2026 This function outputs the <head> element and its contents
    # for the HTML file.

    file_output.write("<head>\n")
    file_output.write("\t<meta charset=\"utf-8\">\n")
    file_output.write(f"\t<meta name=\"description\" content=\"A reference sheet containing {get_language(table_language)} {word_type}s\">\n")
    file_output.write(f"\t<title>Language Reference Sheet: {get_language(table_language)} {word_type}s</title>\n")
    file_output.write("</head>\n")

def html_body(file_output, table_language, word_type, column_headers, data_rows):
    # 20/03/2026 This function outputs the <body> element and its contents
    # for the HTML file
    file_output.write("<body>\n")
    file_output.write("<header></header>\n")
    file_output.write("<nav></nav>\n")
    file_output.write("<main>\n")
    file_output.write(f"<table id=\"{table_language}_{word_type}\">\n")
    file_output.write(f"\t<caption>{get_language(table_language)} {word_type.capitalize()}s</caption>\n")    
    cell_languages = build_cell_languages(table_language, word_type, len(column_headers))    
    write_table(data_rows, column_headers, format_html, file_output, None, cell_languages, table_language)
    file_output.write("\n\t</tbody>\n\t<tfoot>\n\t<tr></tr>\n\t</tfoot>\n")
    file_output.write("</table>\n")
    file_output.write("</main>\n")
    file_output.write("<footer></footer>\n")
    file_output.write("</body>\n")

def build_cell_languages(table_language, word_type, row_length):
    cell_languages = ["en"]

    if word_type == "noun":
        cell_languages += [table_language.lower()] * (row_length - 2)
        cell_languages.append("en")
    else:
        cell_languages += [table_language.lower()] * (row_length - 1)
    return cell_languages
