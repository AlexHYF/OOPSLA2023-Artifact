#!/usr/bin/env python3

########################################################################################################################
# Count number of synth-fun and define-fun commands in a sequence of commands

# Use scripts/holeEnumerator.sh to invoke directly from the command line.

# scripts/funCounter.py < file.sl

# Prints the computed quantities to stdout

########################################################################################################################
# 1. Preamble

import base
from sygusast import *
import sygusfmt

import logging
import platform
import sys

####

assert __name__ == '__main__'
logging.info(f'Hello! (Platform: {platform.python_implementation()} {platform.python_version()})')

####

cmds = sys.stdin.read()
cmds = sygusfmt.deserialize(cmds)

########################################################################################################################

numSynthFun = len(tuple(cmd for cmd in cmds if isinstance(cmd, SynthFunCmd)))
numDefFun = len(tuple(cmd for cmd in cmds if isinstance(cmd, DefineFunCmd)))

print(f'{numSynthFun}, {numDefFun}')
