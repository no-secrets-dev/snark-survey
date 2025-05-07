#!/bin/bash
set -euo pipefail

# Get absolute paths
script_dir="$(dirname "$(readlink -f "$0")")"
root_dir="$(dirname "$script_dir")"
tex_file="${root_dir}/main.tex"
output_dir="${root_dir}/out"
latexmkrc="${root_dir}/latexmkrc"

# Ensure output directory exists
[[ -d "$output_dir" ]] || mkdir -p "$output_dir"

if [[ ! -f "$latexmkrc" ]]; then
    cat > "$latexmkrc" << EOF
\$pdf_mode = 1;
\$bibtex_use = 2;
\$ENV{'BIBINPUTS'}='${root_dir}:' . \$ENV{'BIBINPUTS'};
EOF
fi

# Run latexmk from root directory to use existing latexmkrc
cd "$root_dir"

eval "$(conda shell.bash hook)"

# conda activate web3-env
# python scripts/snarks_table.py
# conda deactivate

latexmk -pdf \
    -synctex=1 \
    -interaction=nonstopmode \
    -file-line-error \
    -outdir="$output_dir" \
    -bibtex \
    "$tex_file"

echo "LaTeX compilation completed successfully"
