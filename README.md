# Off by one
A word game

This repo houses the front end and code to generate the data.

## Front end
Vanilla JS/HTML/CSS.

## Data
 - `parse_data.py` wrangles data sources into a single word list.
 - `find_pairs.py` parses this and outputs a list of patterns (`_at`) and matches (`fat cat sat mat`)
 - `patterns.csv` is the list of all patterns with multiple matches, with clues (hand written).

## Build
The HTML/JS/CSS and data are all built into a single file.
