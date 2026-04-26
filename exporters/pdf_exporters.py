from pathlib import Path
import subprocess
from formatters.latex_formatters import format_latex
from exporters.common_exporters import write_table, write_rows_only
from exporters.latex_exporters import export_latex_file

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
