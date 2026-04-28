# Created 28/04/2025
# Modified 28/04/2025. formatters_csv and write_table() no longer needed;
# csv package accomplishes all that without a problem.
from pathlib import Path
from utils.headers import clean_heading
import csv

def export_csv_file(column_headers, data_rows, table_language, word_type):
    # 28/04/2026 This function takes the data that has been read into the
    # cursor variable and outputs it to a set of comma-separated values.
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)    
    file_name = f"{table_language}_{word_type}.csv"
    file_path = output_dir / file_name
    with open(file_path, "w", newline="", encoding="utf-8-sig") as file_output:
        writer = csv.writer(file_output)
        writer.writerow([clean_heading(col, table_language) for col in column_headers])
        writer.writerows(data_rows)
