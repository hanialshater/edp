#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python scripts/make_figures.py
cd paper
pdflatex -halt-on-error -interaction=nonstopmode paper.tex
pdflatex -halt-on-error -interaction=nonstopmode paper.tex
rm -f paper.aux paper.log paper.out paper.toc paper.fls paper.fdb_latexmk
printf 'built paper/paper.pdf\n'
