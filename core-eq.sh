#!/usr/bin/env bash
# extract-core-equations.sh
# Usage: ./extract-core-equations.sh path/to/name.tex
#
# What it does:
#   1) Finds \begin{align}...\end{align} blocks with \label{<num>:core...}
#   2) Emits valid LaTeX file containing those equations as:
#        \begin{equation}\begin{aligned}...\end{aligned}\tag{<num}}\end{equation}
#   3) Creates a NEW timestamped folder under the "class" directory (like new-entry.sh)
#   4) If a general parser python file exists beside this script (default: core_eqs.py),
#      it will IMPORT that file's CoreEqs, parse the new *-equations.tex, and
#      CODE-GENERATE a Python module with a class of callable methods for each equation line.
#
# Env knobs:
#   AUTO_OPEN=finder|code|none  (default: none)
#   CORE_EQS_PY=/abs/path/to/general_parser.py  (default: <this_dir>/core_eqs.py)

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 INPUT.tex" >&2
  exit 1
fi

IN="$1"
[[ -f "$IN" ]] || { echo "Input not found: $IN" >&2; exit 1; }
[[ "$IN" == *.tex ]] || { echo "Input must be a .tex file" >&2; exit 1; }

# Paths/context
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IN_DIR="$(cd "$(dirname "$IN")" && pwd)"
IN_BASE="$(basename "$IN" .tex)"
CLASS_DIR="$(dirname "$IN_DIR")"   # parent of the entry dir, per your layout

AUTO_OPEN="${AUTO_OPEN:-none}"
CORE_EQS_PY="${CORE_EQS_PY:-$SCRIPT_DIR/core_eqs.py}"

# Prefer venv Python if available
PYBIN="${VIRTUAL_ENV:+$VIRTUAL_ENV/bin/python}"
PYBIN="${PYBIN:-$(command -v python3)}"

# New timestamped folder (with collision handling like new-entry.sh)
TIMESTAMP="$(date +%Y%m%d%H%M)"
FOLDER="$TIMESTAMP"
i=1
while [[ -d "$CLASS_DIR/$FOLDER" ]]; do
  FOLDER="${TIMESTAMP}.$i"; ((i++))
done
ENTRY_DIR="$CLASS_DIR/$FOLDER"
FIG_DIR="$ENTRY_DIR/Figures"
mkdir -p "$FIG_DIR"

OUT_TEX="$ENTRY_DIR/${IN_BASE}-equations.tex"
OUT_GEN="$ENTRY_DIR/${IN_BASE}_core.py"     # <-- generated class file

TMP_CONTENT="$(mktemp)"
trap 'rm -f "$TMP_CONTENT"' EXIT

# --- Collect align blocks with :core labels and emit as equation+aligned+tag ---
# --- Collect align blocks with :core labels and emit as equation+aligned+tag ---
perl -0777 -ne '
  while (m/\\begin\{align\}(.+?)\\end\{align\}/sg) {
    my $blk = $1;
    if ($blk =~ /\\label\{([^}:]+):core[^}]*\}/s) {
      my $tag = $1;  # e.g., 12.68

      # --- PRE-NORMALIZE COMMON FAULTS ---------------------------------------
      # 1) remove :core labels (we’ll tag outside)
      $blk =~ s/\\label\{[^}]*:core[^}]*\}//g;

      # 2) strip \left and \right
      $blk =~ s/\\left\s*//g;
      $blk =~ s/\\right\s*//g;

      # 3) remove align markers
      $blk =~ s/&//g;

      # 4) normalize subscripts with \text{} or \mathrm{}  -> plain
      $blk =~ s/_\{\s*\\(?:text|mathrm)\{([^}]+)\}\s*\}/_{\1}/g;

      # 5) ungroup (X)_{...} -> X_{...}   (simple base)
      $blk =~ s/\(\s*([A-Za-z\\][A-Za-z0-9]*)\s*\)_\{([^}]+)\}/$1_{\2}/g;

      # 6) collapse comma subscripts: _{a,b} -> _{a_b}  (iterate)
      1 while ($blk =~ s/_\{([^}]+),\s*([^}]+)\}/_{\1_\2}/g);

      # 7) dotted symbols: \dot{W} -> Wdot ; \dot{p_c} -> p_cdot
      $blk =~ s/\\dot\{([A-Za-z](?:_[A-Za-z0-9]+|\_\{[^}]+\})?)\}/$1dot/g;

      # 8) tidy products like R\left(T_{cns}\right) -> R T_{cns}
      $blk =~ s/([A-Za-z])\s*\(\s*([A-Za-z][A-Za-z0-9]*(?:_\{[^}]+\}|_[A-Za-z0-9]+)?)\s*\)/$1 $2/g;
      
      $blk =~ s/_(?!\{)([A-Za-z0-9])/_{\1}/g;
      $blk =~ s/\^([A-Za-z0-9])/\^{\1}/g;

      # 9) split chained equalities A=B=C into two lines (A=B \\ newline B=C)
      #    only inside individual lines to keep alignment sane
      $blk =~ s/^\s*(.+?)\s*=\s*(.+?)\s*=\s*(.+?)\s*$/$1 = $2 \\\\\n$2 = $3/gm;

      # trim
      $blk =~ s/^\s+|\s+$//g;

      # --- EMIT CLEAN BLOCK ---------------------------------------------------
      print "\\begin{equation}\n";
      print "\\begin{aligned}\n$blk\n\\end{aligned}\n";
      print "\\tag{$tag}\n";
      print "\\end{equation}\n\n";
    }
  }
' "$IN" > "$TMP_CONTENT"

DATE_ISO="$(date +%Y-%m-%d)"

# --- Write LaTeX wrapper ---
cat >"$OUT_TEX" <<EOF
\\documentclass[12pt]{article}

%––––– Packages –––––
\\usepackage[margin=1in]{geometry}
\\usepackage{amsmath,amssymb,amsthm}
\\usepackage{enumitem}
\\usepackage{hyperref}
\\usepackage{xcolor}
\\usepackage{import}
\\usepackage{xifthen}
\\usepackage{pdfpages}
\\usepackage{transparent}
\\usepackage{listings}
\\usepackage{tikz}
\\usepackage{physics}
\\usepackage{siunitx}
\\usepackage{booktabs}
\\usepackage{cancel}
  \\usetikzlibrary{calc,patterns,arrows.meta,decorations.markings}

\\newcommand{\\incfig}[1]{%%
    \\def\\svgwidth{\\columnwidth}%%
    \\import{./Figures/}{##1.pdf_tex}%%
}

\\theoremstyle{definition}
\\newtheorem{definition}{Definition}
\\newtheorem{example}{Example}
\\newtheorem{problem}{Problem}
\\newtheorem{solution}{Solution}
\\newtheorem{remark}{Remark}
\\theoremstyle{plain}
\\newtheorem{theorem}{Theorem}
\\newtheorem{lemma}{Lemma}
\\newtheorem{proposition}{Proposition}
\\newtheorem{corollary}{Corollary}

\\title{Core Equations — ${IN_BASE}}
\\author{Jerich Lee}
\\date{${DATE_ISO}}

\\begin{document}
\\maketitle

% Auto-extracted equations from align environments with labels ending in :core
EOF

if [[ -s "$TMP_CONTENT" ]]; then
  cat "$TMP_CONTENT" >> "$OUT_TEX"
else
  cat >>"$OUT_TEX" <<'EOF'
\begin{center}
\textit{No \texttt{\textbackslash begin\{align\}} blocks with labels of the form \texttt{\textbackslash label\{\#:\!core\}} were found.}
\end{center}
EOF
fi

cat >>"$OUT_TEX" <<'EOF'

\end{document}
EOF

echo "✔ Created entry folder: $ENTRY_DIR"
echo "✔ Wrote: $OUT_TEX"

# --- Codegen: if the general parser file exists, import it and generate a class module
if [[ -f "$CORE_EQS_PY" ]]; then
"$PYBIN" - "$CORE_EQS_PY" "$OUT_TEX" "$OUT_GEN" "$IN_BASE" <<'PYCODE'
import sys, os, importlib.util, textwrap
from datetime import datetime

core_path, tex_path, out_py, in_base = sys.argv[1:5]

# Import the general parser module from a file path
spec = importlib.util.spec_from_file_location("core_eqs_mod", core_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)  # provides mod.CoreEqs

ce = mod.CoreEqs.from_tex(tex_path)

# Safe Python identifier for class name & method names
def safe_name(s: str, prefix="t"):
    import re
    s2 = re.sub(r'[^0-9a-zA-Z_]', '_', s)
    if not s2 or s2[0].isdigit():
        s2 = f"{prefix}_{s2}"
    return s2

# Class name based on input base name
ClassName = safe_name(in_base.replace('-', '_').replace('.', '_')) + "_Core"

# Precompute srepr strings of residuals, so generated module is standalone
import sympy as sp
srepr_map = {}      # tag -> [srepr residuals...]
sym_names_map = {}  # tag -> [ [sym_name,...], ... ]
for tag in ce.tags():
    reps = []
    symnames = []
    for r in ce.residuals[tag]:
        reps.append(sp.srepr(sp.sympify(r)))
        symnames.append(sorted([s.name for s in r.free_symbols]))
    srepr_map[tag] = reps
    sym_names_map[tag] = symnames

with open(out_py, "w", encoding="utf-8") as f:
    # Header + class start
    f.write(f"""#!/usr/bin/env python3
# Auto-generated on {datetime.now().isoformat(timespec='seconds')}
# Source: {os.path.basename(tex_path)}
# NOTE: This file is standalone; it reconstructs SymPy expressions from srepr strings.
from __future__ import annotations
from typing import Dict, List
import sympy as sp

__all__ = ["{ClassName}"]

class {ClassName}:
    \"\"\"Callable symbolic core equations.

    Access:
      - tags() -> List[str]
      - residual(tag: str, i: int, **subs) -> sp.Expr
      - symbols(tag: str, i: int) -> List[sp.Symbol]
      - eq_all(tag: str) -> List[sp.Expr]
      - Convenience per-line methods: eq_<tag>_<i>(**subs)
    \"\"\"

    _SREPR: Dict[str, List[str]] = {{
""")
    # _SREPR content
    for tag, reps in srepr_map.items():
        f.write(f"        {repr(tag)}: [\n")
        for r in reps:
            f.write("            " + repr(r) + ",\n")
        f.write("        ],\n")
    f.write("    }\n\n")

    # _SYMNAMES content
    f.write("    _SYMNAMES: Dict[str, List[List[str]]] = {\n")
    for tag, symnames in sym_names_map.items():
        f.write(f"        {repr(tag)}: {repr(symnames)},\n")
    f.write("    }\n\n")

    # Methods (properly indented INSIDE the class)
    methods = f'''
def __init__(self) -> None:
    self._cache: Dict[tuple, sp.Expr] = {{}}

def tags(self) -> List[str]:
    return sorted(self._SREPR.keys())

def _expr(self, tag: str, i: int) -> sp.Expr:
    key = (tag, i)
    if key in self._cache:
        return self._cache[key]
    try:
        s = self._SREPR[tag][i]
    except (KeyError, IndexError) as e:
        raise KeyError(f"Unknown equation index for tag '{{tag}}' i={{i}}") from e
    expr = eval(s, {{}}, vars(sp))   # reconstruct SymPy expr from srepr
    self._cache[key] = expr
    return expr

def symbols(self, tag: str, i: int) -> List[sp.Symbol]:
    names = self._SYMNAMES.get(tag, [])
    if i < 0 or i >= len(names):
        raise KeyError(f"Unknown equation index for tag '{{tag}}' i={{i}}")
    return [sp.Symbol(n) for n in names[i]]

def residual(self, tag: str, i: int, **subs) -> sp.Expr:
    expr = self._expr(tag, i)
    return expr.subs(subs) if subs else expr

def eq_all(self, tag: str) -> List[sp.Expr]:
    return [ self._expr(tag, i) for i in range(len(self._SREPR.get(tag, []))) ]
'''
    f.write(textwrap.indent(textwrap.dedent(methods), "    "))

    # Per-line convenience methods, also indented inside class
    for tag, reps in srepr_map.items():
        tag_id = safe_name(tag)
        for i in range(len(reps)):
            m = f"""
def eq_{tag_id}_{i}(self, **subs) -> sp.Expr:
    \"\"\"Residual for tag {tag}, line {i}.\"\"\"
    return self.residual({repr(tag)}, {i}, **subs)
"""
            f.write(textwrap.indent(textwrap.dedent(m), "    "))

    # Footer
    f.write(textwrap.dedent(f"""
if __name__ == "__main__":
    core = {ClassName}()
    print("Tags:", core.tags())
    for t in core.tags():
        print(f"\\nTag {{t}} has", len(core._SREPR[t]), "equation(s).")
        if core._SREPR[t]:
            print(" First residual:", core.residual(t, 0))
"""))

print(f"✔ Wrote generated class: {out_py}")
PYCODE
else
  echo "ℹ General parser not found at: $CORE_EQS_PY"
  echo "  Skipping Python codegen. (Set CORE_EQS_PY to override.)"
fi

# Optionally open the folder
case "$AUTO_OPEN" in
  finder) /usr/bin/open "$ENTRY_DIR" ;;
  code)
    if command -v code >/dev/null 2>&1; then
      /usr/bin/env zsh -lc 'code --reuse-window "'"$ENTRY_DIR"'"'
    else
      echo "ℹ VS Code CLI not found; skipping."
    fi
    ;;
  *) : ;;
esac

echo "Done."