#!/usr/bin/env bash

########################################################################################################################
# Run EUSolver on single specification.
# Intended to only be called from get-impls.sh.

########################################################################################################################

BENCH_FILE=$1
BENCHES_DIR=$2
OUT_DIR=$3
TIMEOUT=$4

BENCH_NAME=$( basename -s ".sl" $BENCH_FILE )
BENCH_DIR=$( dirname $BENCH_FILE )
REL_DIR=$( echo $BENCH_DIR | sed "s#$BENCHES_DIR##" )

mkdir -p $OUT_DIR/$REL_DIR/$BENCH_NAME
cp $BENCH_FILE $OUT_DIR/$REL_DIR/$BENCH_NAME/spec-1.sl

echo "Start time: $( date +%s.%N )" >> $OUT_DIR/$REL_DIR/$BENCH_NAME/sygus.log
timeout -k $TIMEOUT $TIMEOUT \
    ./solvers/eusolver/eusolver $OUT_DIR/$REL_DIR/$BENCH_NAME/spec-1.sl \
    > $OUT_DIR/$REL_DIR/$BENCH_NAME/impl-1.sl \
    2>> $OUT_DIR/$REL_DIR/$BENCH_NAME/sygus.log
echo "Exit status: $?" >> $OUT_DIR/$REL_DIR/$BENCH_NAME/sygus.log
echo "End time: $( date +%s.%N )" >> $OUT_DIR/$REL_DIR/$BENCH_NAME/sygus.log
