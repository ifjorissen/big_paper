#!/bin/bash

#@ifjorissen
# Updated 10.31.15
# usage: `./generate_data.sh <START_ORDER> <MAX_ORDER> <BASE> <RUNS>`
# This script generates #RUNS files for each problemsize (START_ORDER-MAX_ORDER + 1 = number of problem sizes)
# which each contain point sets of size BASE^ORDER in 2-D (with rbox) 

QHULLDIR="/Users/ifjorissen/big_paper/big_paper_code/qhull"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DATADIR="/Users/ifjorissen/big_paper/big_paper_code/analysis/data"
START_ORDER=$1
MAX_ORDER=$2
BOUNDS=100
BASE=$3
RUNS=$4

echo "start order: $START_ORDER  max order: $MAX_ORDER bounds: $BOUNDS base: $BASE runs: $RUNS"
cd $QHULLDIR

for (( ORDER=1; ORDER <= $MAX_ORDER; ORDER++ ))
do
  let psize=$((BASE**ORDER))
  echo "command for $psize random points"
  echo "./bin/rbox $psize D2 B${BOUNDS} n  > ps_${BASE}_${ORDER}/qhull/ps_${BASE}_${ORDER}_<RUN-NUMBER>.txt"  
  mkdir -p $DATADIR/ps_${BASE}_${ORDER}/qhull

  for (( COUNT=1; COUNT <= $RUNS; COUNT++ ))
  do
    let perc=$((COUNT*100/RUNS))
    if [ $((perc % 10)) -eq 0 ]; then
      echo "$perc% complete"
    fi
    ./bin/rbox $psize D2 B${BOUNDS} n  > $DATADIR/ps_${BASE}_${ORDER}/qhull/ps_${BASE}_${ORDER}_$COUNT.txt
  done
  echo "made $RUNS files ps_${BASE}_${ORDER}_<RUN#>.txt for problem size ${psize}"
done

