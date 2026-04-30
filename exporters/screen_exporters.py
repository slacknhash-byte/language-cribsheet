from formatters.text_formatters import format_text
from exporters.common_exporters import write_table
from utils.titles import document_title

def output_to_screen(column_headers, data_rows, table_language, word_type):
    # 02/03/2026 This function takes the data that has been read into the
    # cursor variable and outputs it to the screen, inserting a tab between each
    # field and a carriage return and newline after each record.
    # Updated 21/03/2026. Removed loop, added write_rows() call.
    # Updated 25/04/2026/ Removed write_rows() call, added write_table()    
    
    f = None # No filehandling involved in this function.
    col_count = len(data_rows[0])
    column_widths = [
        max(
            max(len(str(row[i])) for row in data_rows),
            len(str(column_headers[i]))
        )
        for i in range(col_count)
    ]    
    print(f"{document_title(table_language, word_type)}\n\n")
    write_table(data_rows, column_headers, format_text, None, column_widths, None, table_language)
