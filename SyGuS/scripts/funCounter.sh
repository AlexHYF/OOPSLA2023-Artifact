#!/usr/bin/env bash

########################################################################################################################
# Script to count synth-fun and define-fun commands

# Intended to be run from any directory.
# funCounter.sh args
# See src/funCounter.py for documentation regarding arguments and usage instructions.

########################################################################################################################

SCRIPT_DIR=`dirname -- "$( realpath -- "$0"; )";`
$SCRIPT_DIR/../src/funCounter.py "$@"
