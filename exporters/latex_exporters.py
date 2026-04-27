from pathlib import Path
from formatters.latex_formatters import format_latex
from exporters.common_exporters import write_table, write_rows_only

def export_latex_file(column_headers, data_rows, table_language, word_type):
    # 03/03/2026 This function takes the data that has been read into the
    # cursor variable and outputs it to a LaTeX file.
    # 18/03/2026 Spun off latex_preamble() and latex_top_matter()
    # 27/04/2026 Switching from pdflatex to LuaLaTeX
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    file_name = f"{table_language}_{word_type}.tex"
    file_path = output_dir / file_name
    with open(file_path,"w",encoding="utf-8") as file_output:
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

def latex_preamble(file_output):
# 18/03/2026. Added function to generate preamble for LaTeX file to reduce size of export_latex_file()
# 15/04/2026. Removed instruction to include fontenc as it doesn't work with pdflatex.
    file_output.write("\\documentclass[a4paper,oneside]{slides}\n")
    file_output.write("\\usepackage{longtable}\n")  
    file_output.write("\\usepackage{fontspec}\n")

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


