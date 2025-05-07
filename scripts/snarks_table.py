import json
import pandas as pd
from pathlib import Path

# Define SNARK characteristics in JSON format - focusing on pairing-based SNARKs
snarks_data = {
    "snarks": [
        {
            "name": "GGPR13",
            "characteristics": {
                "SRS size": "$O(n)$",
                "prover-time": r"$O(n \log n)$",
                "proof-length": r"$7 \mathbb{G}_1 + 1 \mathbb{G}_2 + 1 \mathbb{F}$",
                "verifier-time": "$O(n)$",
                "universal": "No",
                "updatable": "No",
                "sec. model": "CRS",
                "assumptions": "q-PKE, q-PDH"
            }
        },
        {
            "name": "PGHR13",
            "characteristics": {
                "SRS size": "$O(n)$",
                "prover-time": r"$O(n \log n)$",
                "proof-length": r"$7 \mathbb{G}_1 + 1 \mathbb{G}_2$",
                "verifier-time": "$O(n)$",
                "universal": "No",
                "updatable": "No",
                "sec. model": "CRS",
                "assumptions": "q-PDH"
            }
        },
        {
            "name": "Groth16",
            "characteristics": {
                "SRS size": "$O(n)$",
                "prover-time": r"$O(n \log n)$",
                "proof-length": r"$2 \mathbb{G}_1 + 1 \mathbb{G}_2$",
                "verifier-time": "$O(1)$",
                "universal": "No",
                "updatable": "No",
                "sec. model": "CRS",
                "assumptions": "q-type"
            }
        },
        {
            "name": "GMKL18",
            "characteristics": {
                "SRS size": "$O(n^2)$",
                "prover-time": r"$O(n \log n)$",
                "proof-length": r"$O(1) \mathbb{G}_1 + O(1) \mathbb{G}_2 + O(1) \mathbb{F}$",
                "verifier-time": "$O(1)$",
                "universal": "Yes",
                "updatable": "Yes",
                "sec. model": "CRS",
                "assumptions": "SXDH"
            }
        },
        {
            "name": "MBKM19",
            "characteristics": {
                "SRS size": "$O(n)$",
                "prover-time": r"$O(n \log n)$",
                "proof-length": r"$7 \mathbb{G}_1 + 1 \mathbb{G}_2 + 5 \mathbb{F}$",
                "verifier-time": "$O(1)$",
                "universal": "Yes",
                "updatable": "Yes",
                "sec. model": "CRS",
                "assumptions": "SXDH"
            }
        },
        {
            "name": "GWC19",
            "characteristics": {
                "SRS size": "$O(n)$",
                "prover-time": r"$O(n \log n)$",
                "proof-length": r"$7 \mathbb{G}_1 + 1 \mathbb{G}_2$",
                "verifier-time": "$O(1)$",
                "universal": "Yes",
                "updatable": "Yes",
                "sec. model": "CRS",
                "assumptions": "SXDH"
            }
        },
        {
            "name": "CHM+19",
            "characteristics": {
                "SRS size": "$O(n)$",
                "prover-time": r"$O(n \log n)$",
                "proof-length": r"$7 \mathbb{G}_1 + 1 \mathbb{G}_2 + 6 \mathbb{F}$",
                "verifier-time": "$O(1)$",
                "universal": "Yes",
                "updatable": "Yes",
                "sec. model": "CRS",
                "assumptions": "AGM"
            }
        }
    ]
}

def generate_pairing_snark_table():
    # Convert JSON to DataFrame format
    rows = []
    for snark in snarks_data["snarks"]:
        row = {"method": snark["name"]}
        row.update(snark["characteristics"])
        rows.append(row)

    df = pd.DataFrame(rows)

    # Define the columns to include and their format specification
    column_formats = {
        "method": "l",
        "SRS size": "l",
        "prover-time": "l",
        "proof-length": "p{3.2cm}",
        "verifier-time": "l",
        "universal": "c",
        "updatable": "c",
        "sec. model": "l",
        "assumptions": "l"
    }

    # Include only the columns you want to display
    columns_order = ["method", "SRS size", "prover-time", "proof-length", 
                     "verifier-time", "universal", "updatable", "assumptions"]

    # Uncomment and modify this line to exclude a column
    # columns_order.remove("updatable")

    df = df[columns_order]

    # Generate the column format string automatically
    col_format = "|" + "|".join(column_formats[col] for col in columns_order) + "|"

    # Generate LaTeX table
    latex = df.to_latex(
        index=False,
        escape=False,
        column_format=col_format,
        caption='Comparison of Pairing-based SNARK Systems',
        position='H'
    )

    # Fix the table formatting by adding proper lines
    latex_lines = latex.split('\n')

    # Add hline after begin{tabular}
    begin_tabular_idx = next(i for i, line in enumerate(latex_lines) if '\\begin{tabular}' in line)
    latex_lines.insert(begin_tabular_idx + 1, '\\hline')

    # Add toprule after header row
    header_idx = next(i for i, line in enumerate(latex_lines) if '\\\\' in line)
    latex_lines[header_idx] = latex_lines[header_idx].replace('\\\\', '\\\\ \\hline\\toprule')

    # Add midrule after each data row except the last
    data_rows = [i for i, line in enumerate(latex_lines) if '\\\\' in line and i > header_idx]
    for i in data_rows[:-1]:
        latex_lines[i] = latex_lines[i].replace('\\\\', '\\\\ \\hline')

    # Add bottomrule after the last data row
    if data_rows:
        latex_lines[data_rows[-1]] = latex_lines[data_rows[-1]].replace('\\\\', '\\\\ \\hline\\bottomrule')

    latex = '\n'.join(latex_lines)

    # Get script's directory and project root
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    # Write to mainmatter/tables/pairing_snarks.tex
    output_path = project_root / 'tex_files' / 'snark-table.tex'
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        f.write(latex)

    print(f"Table generated at {output_path}")

if __name__ == "__main__":
    generate_pairing_snark_table()
