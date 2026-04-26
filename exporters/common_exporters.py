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
