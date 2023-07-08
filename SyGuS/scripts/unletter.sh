#!/usr/bin/env bash

########################################################################################################################
# Script to inline let expressions from SyGuS files.

# Intended to be run from any directory.
# unletter.sh args
# See src/unletter.py for documentation regarding arguments and usage instructions.

########################################################################################################################

SCRIPT_DIR=`dirname -- "$( realpath -- "$0"; )";`
. $SCRIPT_DIR/../venv/cpython/bin/activate
$SCRIPT_DIR/../src/unletter.py "$@"
