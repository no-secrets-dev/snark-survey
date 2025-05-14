import json
import pandas as pd
from pathlib import Path

# Define column mappings - single source of truth for column names
CAPTION_TEXT = r"""Comparison of work done by pairing-based SNARKs. 
$n$ represents the number of circuit gates; $\mathbb{G}_1$ and 
$\mathbb{G}_2$ represent group elements; $\mathbb{F}$ represents field elements; $\mathbf{P}$ represents pairing operations. 
In prover/verifier work columns, $\mathbb{G}_i$ and $\mathbb{F}$ refer to elliptic curve group scalar multliplications in $\mathbb{G}_i$ 
and field element multiplications in $\mathbb{F}$, respectively. An asterisk implies the method is not fully succinct. Where more fine-grained 
source group information is easily discerned, $\mathbb{G}$ implies the elements / operations could be in either source group.
Where more fine-grained information is not available or easily comparable in a standardized manner, we resort to asymptotic terms."""

COLUMN_MAPPING = {
    "srs_size": {"display": "CRS size (asymp.)", "format": "l"},
    "prover_time": {"display": r"$\mathcal{P}$ work (asymp.)", "format": "l"},
    "proof_length": {"display": r"proof size", "format": "p{3.2cm}"},
    "verifier_time": {"display": r"$\mathcal{V}$ work", "format": "l"},
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
                "srs_size": r"$O(n) \mathbb{G}$",
                "prover_time": r"$O(n) \mathbb{G}$",
                "proof_length": r"$9 \mathbb{G}$",
                "verifier_time": r"$14 \mathbf{P}$",
                "universal": "No",
                "updatable": "No",
                "assumptions": r"q-PKE, q-PDH"
            }
        },
        # {
        #     "name": "PGHR13",
        #     "characteristics": {
        #         "srs_size": r"$O(n) \mathbb{G}_1 / \mathbb{G}_2$",
        #         "prover_time": r"$O(n) \mathbb{G}_1 / \mathbb{G}_2$",
        #         "proof_length": r"$7 \mathbb{G}_1, 2 \mathbb{G}_2$",
        #         "verifier_time": r"$11 \mathbf{P}$",
        #         "universal": "No",
        #         "updatable": "No",
        #         "assumptions": r"$q$-PKE, $q$-PDH"
        #     }
        # },

        {
            "name": "PGHR13",
            "characteristics": {
                "srs_size": r"$O(n) \mathbb{G}$",
                "prover_time": r"$O(n) \mathbb{G}$",
                "proof_length": r"$8 \mathbb{G}$",
                "verifier_time": r"$11 \mathbf{P}$",
                "universal": "No",
                "updatable": "No",
                "assumptions": r"$q$-PKE, $q$-PDH"
            }
        },

        {
            "name": "Groth16",
            "characteristics": {
                "srs_size": r"$9n \mathbb{G}_1, 3n \mathbb{G}_2$",
                "prover_time": r"$n \mathbb{G}_1$",
                "proof_length": r"$2 \mathbb{G}_1, 1 \mathbb{G}_2$",
                "verifier_time": r"$3 \mathbf{P}$",
                "universal": "No",
                "updatable": "No",
                "assumptions": r"$q$-type, GGM"
            }
        },
        {
            "name": "GMKL18",
            "characteristics": {
                "srs_size": r"$O(n^2) \mathbb{G}$",
                "prover_time": r"$O(n) \mathbb{G}_1$",
                "proof_length": r"$2 \mathbb{G}_1, 1 \mathbb{G}_2$",
                "verifier_time": r"$5 \mathbf{P}$",
                "universal": "Yes",
                "updatable": "Yes",
                "assumptions": r"$q$-type, KOE"
            }
        },
        {
            "name": "MBKM19",
            "characteristics": {
                "srs_size": r"$36n \mathbb{G}_1$",
                "prover_time": r"$273n \mathbb{G}_1$",
                "proof_length": r"$20 \mathbb{G}_1, 16 \mathbb{F}$",
                "verifier_time": r"$13 \mathbf{P}$",
                "universal": "Yes",
                "updatable": "Yes",
                "assumptions": "AGM"
            }
        },

        {
            "name": "Gab19*",
            "characteristics": {
                "srs_size": r"$2n \mathbb{G}_1$",
                "prover_time": r"$8n \mathbb{G}_1$",
                "proof_length": r"$6 \mathbb{G}_1, 4 \mathbb{F}$",
                "verifier_time": r"$5 \mathbf{P}$",
                "universal": "Yes",
                "updatable": "Yes",
                "assumptions": "AGM"
            }
        },

        {
            "name": "GWC19",
            "characteristics": {
                "srs_size": r"$3n \mathbb{G}_1, 2 \mathbb{G}_2$",
                "prover_time": r"$11n \mathbb{G}_1$",
                "proof_length": r"$7 \mathbb{G}_1, 6 \mathbb{F}$",
                "verifier_time": r"$2 \mathbf{P}, 16 \mathbb{G}_1$",
                "universal": "Yes",
                "updatable": "Yes",
                "assumptions": "AGM"
            }
        },


        {
            "name": "GW21",
            "characteristics": {
                "srs_size": r"$9n \mathbb{G}_1, 2 \mathbb{G}_2$",
                "prover_time": r"$35n \mathbb{G}_1$",
                "proof_length": r"$4 \mathbb{G}_1, 15 \mathbb{F}$",
                "verifier_time": r"$5 \mathbb{G}_1, 2 \mathbf{P}$",
                "universal": "Yes",
                "updatable": "Yes",
                "assumptions": "AGM"
            }
        },
        {
            "name": "CHM+19",
            "characteristics": {
                "srs_size": r"$(4n +2) \mathbb{G}_1$",
                "prover_time": r"$22n \mathbb{G}_1$",
                "proof_length": r"$13 \mathbb{G}_1, 8 \mathbb{F}$",
                "verifier_time": r"$2 \mathbf{P}$",
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
        caption=CAPTION_TEXT,
        label=r'tbl:snark',
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

    end_table_idx = next(i for i, line in enumerate(latex_lines) if '\\end{table}' in line)
    # latex_lines.insert(end_table_idx, r'\captionsetup{' + r'width=.9' + r'\linewidth}')
    # latex_lines.insert(end_table_idx + 1, r'\caption{' + f'{CAPTION_TEXT}'+ r'}')

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
