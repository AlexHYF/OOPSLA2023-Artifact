#!/usr/bin/env bash

########################################################################################################################
# Main Script

# Intended to be run from any directory.
# run.sh args
# See src/main.py for documentation regarding arguments and usage instructions.

########################################################################################################################

SCRIPT_DIR=`dirname -- "$( realpath -- "$0"; )";`
$SCRIPT_DIR/../src/main.py "$@"
