import json
import pandas as pd
from pathlib import Path

# Define SNARK characteristics in JSON format - focusing on pairing-based SNARKs
snarks_data = {
    "snarks": [
        {
            "name": "GGPR",
            "characteristics": {
                "SRS size": "$O(n)$",
                "prover-runtime": r"$O(n \log n)$",
                "proof-length": "9 group elements",
                "verifier-runtime": "$O(n)$",
                "universal": "No",
                "updatable": "No",
                "security-model": "CRS, q-PKE, q-PDH"
            }
        },
        {
            "name": "Pinocchio",
            "characteristics": {
                "SRS size": "$O(n)$",
                "prover-runtime": r"$O(n \log n)$",
                "proof-length": "8 group elements",
                "verifier-runtime": "$O(n)$",
                "universal": "No",
                "updatable": "No",
                "security-model": "CRS"
            }
        },
        {
            "name": "Groth16",
            "characteristics": {
                "SRS size": "$O(n)$",
                "prover-runtime": r"$O(n \log n)$",
                "proof-length": "3 group elements",
                "verifier-runtime": "$O(1)$",
                "universal": "No",
                "updatable": "No",
                "security-model": "CRS, q-type"
            }
        },
        {
            "name": "Groth-Updatable",
            "characteristics": {
                "SRS size": "$O(n^2)$",
                "prover-runtime": r"$O(n \log n)$",
                "proof-length": "$O(1)$",
                "verifier-runtime": "$O(1)$",
                "universal": "Yes",
                "updatable": "Yes",
                "security-model": "CRS"
            }
        },
        {
            "name": "Sonic",
            "characteristics": {
                "SRS size": "$O(n)$",
                "prover-runtime": r"$O(n \log n)$",
                "proof-length": "$O(1)$",
                "verifier-runtime": "$O(1)$",
                "universal": "Yes",
                "updatable": "Yes",
                "security-model": "CRS"
            }
        },
        {
            "name": "PlonK",
            "characteristics": {
                "SRS size": "$O(n)$",
                "prover-runtime": r"$O(n \log n)$",
                "proof-length": "$O(1)$",
                "verifier-runtime": "$O(1)$",
                "universal": "Yes",
                "updatable": "Yes",
                "security-model": "CRS"
            }
        },
        {
            "name": "Marlin",
            "characteristics": {
                "SRS size": "$O(n)$",
                "prover-runtime": r"$O(n \log n)$",
                "proof-length": "$O(1)$",
                "verifier-runtime": "$O(1)$",
                "universal": "Yes",
                "updatable": "Yes",
                "security-model": "CRS, AGM"
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
    
    # Reorder columns if needed
    columns_order = ["method", "SRS size", "prover-runtime", "proof-length", "verifier-runtime", 
                     "universal", "updatable", "security-model"]
    df = df[columns_order]
    
    # Generate LaTeX table
    latex = df.to_latex(
        index=False,
        escape=False,
        column_format='|l|l|l|l|l|c|c|l|',
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
