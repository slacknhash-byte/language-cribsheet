from pathlib import Path
from formatters.text_formatters import format_text
from exporters.common_exporters import write_table

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
