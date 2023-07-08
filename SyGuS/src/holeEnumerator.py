#!/usr/bin/env python3

########################################################################################################################
# Enumerate holes in implementations

# Use scripts/holeEnumerator.sh to invoke directly from the command line.

# scripts/holeEnumerator.py < impl.sl > holes.txt

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

impl = sys.stdin.read()
impl = sygusfmt.deserialize(impl)

########################################################################################################################

def mapTerm(term):
    assert isinstance(term, Term)

    yield (-1,)

    ####

    if isinstance(term, VarTerm): pass

    elif isinstance(term, FunAppTerm):
        for i, t in enumerate(term.args):
            for addr in mapTerm(t):
                yield (i + 1,) + addr

    elif isinstance(term, LetTerm): assert False

    elif isinstance(term, Literal): pass

    else: assert False

########################################################################################################################

# Final Script

for i, cmd in enumerate(impl):
    assert isinstance(cmd, DefineFunCmd)

    for addr in mapTerm(cmd.term):
        addr = (i, 4) + addr
        addr = (str(j) for j in addr)
        addr = ' '.join(addr)
        print(addr)
