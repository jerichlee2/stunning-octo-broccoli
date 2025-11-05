#!/usr/bin/env bash
# new-entry.sh — create a course entry under the detected term folder (no git)

set -euo pipefail

# --- Locate the term folder (parent of this script's directory) ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TERM_DIR="$(dirname "$SCRIPT_DIR")"   # .../classes/04_fall_2025

# Optional: auto-open the new folder (finder | code | none)
AUTO_OPEN="${AUTO_OPEN:-none}"

slugify() {
  printf '%s\n' "$1" \
    | tr '[:upper:]' '[:lower:]' \
    | tr -s '[:space:]' '-' \
    | tr -cd '[:alnum:]-_' \
    | sed -e 's/^-*//' -e 's/-*$//'
}

# --- Prompts ---
read -rp "Class name: " CLASS
CLASS_SLUG=$(slugify "$CLASS")

read -rp "Title: " TITLE
TITLE_SLUG=$(slugify "$TITLE")

read -rp "Topic (optional): " TOPIC || true
read -rp "Tags (comma-separated, optional): " TAGS || true

# --- Paths / names ---
DATE_ISO=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%Y%m%d%H%M)

COURSE_DIR="$TERM_DIR/$CLASS_SLUG"        # e.g. .../04_fall_2025/me-420
mkdir -p "$COURSE_DIR"

FOLDER="$TIMESTAMP"
i=1
while [[ -d "$COURSE_DIR/$FOLDER" ]]; do
  FOLDER="${TIMESTAMP}.$i"; ((i++))
done

ENTRY_DIR="$COURSE_DIR/$FOLDER"
FIG_DIR="$ENTRY_DIR/Figures"
mkdir -p "$FIG_DIR"

BASENAME="$TITLE_SLUG"
TEX_PATH="$ENTRY_DIR/$BASENAME.tex"
PY_PATH="$ENTRY_DIR/$BASENAME.py"

# --- Write LaTeX stub ---
cat >"$TEX_PATH" <<EOF
\\documentclass[12pt]{article}
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

\\title{$TITLE}
\\author{Jerich Lee}
\\date{$DATE_ISO}

\\begin{document}
\\maketitle
\\tableofcontents
% Course: $CLASS
% Topic:  $TOPIC
% Tags:   $TAGS

% Your content here.

\\end{document}
EOF

# --- Write Python stub ---
cat >"$PY_PATH" <<EOF
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: $TITLE
Class: $CLASS
Date:  $DATE_ISO
"""

def main() -> None:
    print("Hello, World!")

if __name__ == "__main__":
    main()
EOF
chmod +x "$PY_PATH"

echo "Created: $TEX_PATH"
echo "Created: $PY_PATH"
echo "Entry folder: $ENTRY_DIR"

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