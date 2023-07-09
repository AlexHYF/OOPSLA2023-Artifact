#!/usr/bin/env bash


SCRIPT_DIR=`dirname -- "$( realpath -- "$0"; )";`
TEMP=$(mktemp) 
#echo $1
cat $1 |  python3 $SCRIPT_DIR/src/unletter.py 1>$TEMP #2>/dev/null
$SCRIPT_DIR/src/main.py $TEMP $2 #2>/dev/null
