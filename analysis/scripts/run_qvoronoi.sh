#!/bin/bash

# Updated 10.31.15
# usage `./run_qvoronoi.sh`
# This script runs q_voronoi on each of the files in the dataset
# and pipes the output to a results folder where it will be extracted

QHULLDIR="/Users/ifjorissen/big_paper/big_paper_code/qhull"
DATADIR="/Users/ifjorissen/big_paper/big_paper_code/analysis/data"
RESULTDIR="/Users/ifjorissen/big_paper/big_paper_code/analysis/results"

mkdir -p $DATADIR/ps${psize}/qhull
