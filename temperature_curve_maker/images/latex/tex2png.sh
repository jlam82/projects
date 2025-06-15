#!/bin/bash

file="${1%.tex}" # get filename without extension
latex "$file.tex" || exit 1 # compile .tex to .dvi
dvipng -D 300 -T tight -o "$file.png" "$file.dvi" || exit 1 # convert .dvi to .png using dvipng
convert "$file.png" -bordercolor white -border 2 "$file.png" || exit 1 # add 2px white border
