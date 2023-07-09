#!/bin/bash
SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
SPECPATH=$(realpath $1)
$SCRIPTPATH/solvers/eusolver/eusolver $SPECPATH | $SCRIPTPATH/src/unletter.py 2>/dev/null
