from pathlib import Path
from exporters.common_exporters import write_table
from utils.titles import document_title, build_codename
from utils.headers import clean_heading, get_language

def export_markdown_file(column_headers, data_rows, table_language, word_type):
    # 01/05/2026 This function takes the data that has been read into the
    # cursor variable and outputs it in markdown format.

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)    
    file_name = f"{table_language}_{word_type}.md"
    file_path = output_dir / file_name
    with open(file_path,"w",encoding="utf-8-sig") as file_output:
        col_count = len(data_rows[0])
        column_widths = [
            max(
                max(len(str(row[i])) for row in data_rows),
                len(str(column_headers[i]))
            )
            for i in range(col_count)
        ]
        file_output.write(f"# {document_title(table_language, word_type)}\n\n")
        write_markdown_table(column_headers, data_rows, file_output, table_language)
        file_output.write(f"Reference Number: {build_codename(table_language,word_type)}")

def write_markdown_table(column_headers, data_rows, file_output, table_language):
    # Header
    row = [clean_heading(str(field), table_language).capitalize() for field in column_headers]
    file_output.write("| " + " | ".join(row) + " |\n")

    # Separator
    file_output.write("|" + "|".join(["---"] * len(column_headers)) + "|\n")

    # Rows
    for row in data_rows:
        file_output.write("| " + " | ".join(str(v) for v in row) + " |\n\n")
