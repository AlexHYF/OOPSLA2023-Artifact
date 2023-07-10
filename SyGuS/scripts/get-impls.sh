#!/usr/bin/env bash

########################################################################################################################
# Record of running CVC5 and EUSolver on all 2017 SyGuS benchmarks

BENCHES_DIR=./tests/sygus-benchmarks/comp/2017
TIMEOUT=300s

NUM_SOCKETS=$( lscpu | grep 'Socket(s):' | sed 's/.*: *//' )
NUM_CORES_PER_SOCKET=$( lscpu | grep 'Core(s) per socket:' | sed 's/.*: *//' )
NPROC=$( expr $NUM_SOCKETS '*' $NUM_CORES_PER_SOCKET ) # 10, or 16

OUT_DIR=impls
mkdir -p $OUT_DIR
echo "BENCHES_DIR: $BENCHES_DIR" | tee -a $OUT_DIR/get-impls.log
echo "NPROC: $NPROC" | tee -a $OUT_DIR/get-impls.log
echo "TIMEOUT: $TIMEOUT" | tee -a $OUT_DIR/get-impls.log

########################################################################################################################
# 1. Run the solvers

tsp -S $NPROC

####

OUT_DIR=impls/cvc5
mkdir -p $OUT_DIR
echo "OUT_DIR: $OUT_DIR" | tee -a $OUT_DIR/get-impls.log
find $BENCHES_DIR -name '*.sl' \
                  -exec tsp ./scripts/get-impl-cvc5.sh {} "$BENCHES_DIR" "$OUT_DIR" "$TIMEOUT" \;

####

OUT_DIR=impls/eusolver
mkdir -p $OUT_DIR
echo "OUT_DIR: $OUT_DIR" | tee -a $OUT_DIR/get-impls.log
find $BENCHES_DIR -name '*.sl' \
                  -exec tsp ./scripts/get-impl-eusolver.sh {} "$BENCHES_DIR" "$OUT_DIR" "$TIMEOUT" \;
