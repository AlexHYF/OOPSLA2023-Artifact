#!/bin/sh
SCRIPT=$(realpath -s "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
$SCRIPTPATH/solvers/cvc5/build/bin/cvc4 --lang=sygus1 $@ | python3 $SCRIPTPATH/src/unletter.py 2>/dev/null
