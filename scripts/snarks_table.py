import json
import pandas as pd
from pathlib import Path

# Define column mappings - single source of truth for column names
COLUMN_MAPPING = {
    "srs_size": {"display": "CRS size", "format": "l"},
    "proof_length": {"display": r"proof size", "format": "p{3.2cm}"},
    "prover_time": {"display": r"$T(\mathcal{P})$", "format": "l"},
    "verifier_time": {"display": r"$T(\mathcal{V})$", "format": "l"},
    "universal": {"display": "universal", "format": "c"},
    "updatable": {"display": "updatable", "format": "c"},
    "assumptions": {"display": "assumptions", "format": "l"}
}

# Use internal keys in the data structure
snarks_data = {
    "snarks": [
        {
            "name": "GGPR13",
            "characteristics": {
                "srs_size": "$O(n)$",
                "prover_time": r"$O(n \log n)$",
                "proof_length": r"$9 \mathbb{G}_1$",
                "verifier_time": r"$O(\ell)$",
                "universal": "No",
                "updatable": "No",
                "assumptions": "q-PKE, q-PDH"
            }
        },
        {
            "name": "PGHR13",
            "characteristics": {
                "srs_size": "$O(n)$",
                "prover_time": r"$O(n \log n)$",
                "proof_length": r"$8 \mathbb{G}_1$",
                "verifier_time": r"$O(\ell)$",
                "universal": "No",
                "updatable": "No",
                "assumptions": "q-PDH"
            }
        },
        {
            "name": "Groth16",
            "characteristics": {
                "srs_size": "$O(n)$",
                "prover_time": r"$O(n \log n)$",
                "proof_length": r"$2 \mathbb{G}_1, 1 \mathbb{G}_2$",
                "verifier_time": r"$O(\ell)$",
                "universal": "No",
                "updatable": "No",
                "assumptions": "q-type, KOE"
            }
        },
        {
            "name": "GMKL18",
            "characteristics": {
                "srs_size": "$O(n^2)$",
                "prover_time": r"$O(n \log n)$",
                "proof_length": r"$2 \mathbb{G}_1, 1 \mathbb{G}_2$",
                "verifier_time": "$O(1)$",
                "universal": "Yes",
                "updatable": "Yes",
                "assumptions": "q-type, KOE"
            }
        },
        {
            "name": "MBKM19 (helped)",
            "characteristics": {
                "srs_size": "$O(n)$",
                "prover_time": r"$O(n \log n)$",
                "proof_length": r"$7 \mathbb{G}_1, 5 \mathbb{F}$",
                "verifier_time": "$O(1)$",
                "universal": "Yes",
                "updatable": "Yes",
                "assumptions": "AGM"
            }
        },
        {
            "name": "MBKM19 (unhelped)",
            "characteristics": {
                "srs_size": "$O(n)$",
                "prover_time": r"$O(n \log n)$",
                "proof_length": r"$20 \mathbb{G}_1, 16 \mathbb{F}$",
                "verifier_time": "$O(1)$",
                "universal": "Yes",
                "updatable": "Yes",
                "assumptions": "AGM"
            }
        },
        {
            "name": "GWC19",
            "characteristics": {
                "srs_size": "$O(n)$",
                "prover_time": r"$O(n \log n)$",
                "proof_length": r"$9 \mathbb{G}_1, 6 \mathbb{F}$",
                "verifier_time": "$O(1)$",
                "universal": "Yes",
                "updatable": "Yes",
                "assumptions": "AGM"
            }
        },
        {
            "name": "CHM+19",
            "characteristics": {
                "srs_size": "$O(n)$",
                "prover_time": r"$O(n \log n)$",
                "proof_length": r"$13 \mathbb{G}_1, 8 \mathbb{F}$",
                "verifier_time": "$O(1)$",
                "universal": "Yes",
                "updatable": "Yes",
                "assumptions": "AGM"
            }
        }
    ]
}

def generate_pairing_snark_table():
    # Convert JSON to DataFrame using internal keys
    rows = []
    for snark in snarks_data["snarks"]:
        row = {"method": snark["name"]}
        row.update(snark["characteristics"])
        rows.append(row)

    df = pd.DataFrame(rows)
    
    # Rename columns for display using our mapping
    df.rename(columns={k: v["display"] for k, v in COLUMN_MAPPING.items()}, inplace=True)
    
    # Define column order based on mapping (keeps "method" first)
    columns_order = ["method"] + [v["display"] for k, v in COLUMN_MAPPING.items()]
    
    # Filter df to include only specified columns in the right order
    df = df[columns_order]
    
    # Generate column format string from mapping
    col_format = "|l|" + "|".join(v["format"] for v in COLUMN_MAPPING.values()) + "|"
    
    # Generate LaTeX table
    latex = df.to_latex(
        index=False,
        escape=False,
        column_format=col_format,
        caption='Comparison of Pairing-based SNARK Systems',
        position='!t'
    )

    # Fix the table formatting by adding proper lines
    latex_lines = latex.split('\n')

    # Add hline after begin{tabular}
    begin_tabular_idx = next(i for i, line in enumerate(latex_lines) if '\\begin{tabular}' in line)
    latex_lines.insert(begin_tabular_idx + 1, '\\hline')

    # Add toprule after header row
    header_idx = next(i for i, line in enumerate(latex_lines) if '\\\\' in line)
    latex_lines[header_idx] = latex_lines[header_idx].replace('\\\\', '\\\\ \\hline\\toprule')

    # Add midrule after each data row
    data_rows = [i for i, line in enumerate(latex_lines) if '\\\\' in line and i > header_idx]
    for i in data_rows[:-1]:
        latex_lines[i] = latex_lines[i].replace('\\\\', '\\\\ \\hline')

    # Add bottomrule after the last data row
    if data_rows:
        latex_lines[data_rows[-1]] = latex_lines[data_rows[-1]].replace('\\\\', '\\\\ \\hline\\bottomrule')
        # Add one more bottomrule for extra emphasis
        latex_lines.insert(data_rows[-1] + 1, '\\bottomrule')

    latex = '\n'.join(latex_lines)

    # Get script's directory and project root
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    # Write to tex_files/snark-table.tex
    output_path = project_root / 'tex_files' / 'snark-table.tex'
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        f.write(latex)

    print(f"Table generated at {output_path}")

if __name__ == "__main__":
    generate_pairing_snark_table()
