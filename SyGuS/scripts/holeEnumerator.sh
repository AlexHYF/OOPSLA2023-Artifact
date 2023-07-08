#!/usr/bin/env bash

########################################################################################################################
# Script to enumerate holes in implementations

# Intended to be run from any directory.
# holeEnumerator.sh args
# See src/holeEnumerator.py for documentation regarding arguments and usage instructions.

########################################################################################################################

SCRIPT_DIR=`dirname -- "$( realpath -- "$0"; )";`
. $SCRIPT_DIR/../venv/cpython/bin/activate
$SCRIPT_DIR/../src/holeEnumerator.py "$@"
