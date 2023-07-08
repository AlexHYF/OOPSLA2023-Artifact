#!/usr/bin/env bash

########################################################################################################################
# Record of running CVC5 and EUSolver on all 2017 SyGuS benchmarks

PER_IMPL_TIMEOUT=1800s
export PER_HOLE_TIMEOUT=300s
MAX_HOLES=100

NUM_SOCKETS=$( lscpu | grep 'Socket(s):' | sed 's/.*: *//' )
NUM_CORES_PER_SOCKET=$( lscpu | grep 'Core(s) per socket:' | sed 's/.*: *//' )
NPROC=$( expr $NUM_SOCKETS '*' $NUM_CORES_PER_SOCKET ) # 10, or 16

########################################################################################################################
# 1. Run the solvers

tsp -S $NPROC

####

SOLVER=cvc5
BASE_DIR=impls/$SOLVER

find $BASE_DIR -name 'run.out' -exec rm {} \;
find $BASE_DIR -name 'run.log' -exec rm {} \;

for i in `find $BASE_DIR -name 'spec-2.sl'`; do
    BENCH=$( echo $i | sed "s/.*impls\/$SOLVER\///" | sed 's/\/spec-2\.sl$//' )
    if [[ $( cat $BASE_DIR/$BENCH/holes.txt | wc -l ) -le $MAX_HOLES ]]; then
        tsp ./scripts/run2.sh $BASE_DIR $BENCH $PER_IMPL_TIMEOUT
    fi
done

####

SOLVER=eusolver
BASE_DIR=impls/$SOLVER

find $BASE_DIR -name 'run.out' -exec rm {} \;
find $BASE_DIR -name 'run.log' -exec rm {} \;

for i in `find $BASE_DIR -name 'spec-2.sl'`; do
    BENCH=$( echo $i | sed "s/.*impls\/$SOLVER\///" | sed 's/\/spec-2\.sl$//' )
    if [[ $( cat $BASE_DIR/$BENCH/holes.txt | wc -l ) -le $MAX_HOLES ]]; then
        tsp ./scripts/run2.sh $BASE_DIR $BENCH $PER_IMPL_TIMEOUT
    fi
done
