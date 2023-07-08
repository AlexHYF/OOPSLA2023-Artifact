#!/usr/bin/env bash

########################################################################################################################
# Invoke run.sh for a single benchmark.
# Intended to only be invoked from do-runs.sh.

########################################################################################################################

BASE_DIR=$1
BENCH=$2
PER_IMPL_TIMEOUT=$3

echo Start time: $( date +%s.%N ) > $BASE_DIR/$BENCH/run.log

timeout -k $PER_IMPL_TIMEOUT $PER_IMPL_TIMEOUT \
    ./run.sh $BASE_DIR/$BENCH/spec-2.sl $BASE_DIR/$BENCH/impl-2.sl \
        < $BASE_DIR/$BENCH/holes.txt \
        > $BASE_DIR/$BENCH/run.out 2>> $BASE_DIR/$BENCH/run.log
STATUS=$?

echo Exit status: $STATUS >> $BASE_DIR/$BENCH/run.log
echo End time: $( date +%s.%N ) >> $BASE_DIR/$BENCH/run.log 
