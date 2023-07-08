#!/usr/bin/env python3

########################################################################################################################
# Remove let-expressions from SyGuS problem instance

# May be invoked either directly from the command line, or used via the unletCmd function defined here.
# In the former case, this script reads its input from stdin and prints its output to stdout.

# scripts/unletter.py < spec-1.sl > spec-2.sl

########################################################################################################################
# 1. Preamble

import base
from sygusast import *
import sygusfmt

import logging
import platform
import sys

########################################################################################################################

def unletCmd(cmd):
    assert isinstance(cmd, Cmd)
    if isinstance(cmd, DeclareVarCmd): return cmd
    elif isinstance(cmd, ConstraintCmd): return ConstraintCmd(unletTerm(cmd.term))
    elif isinstance(cmd, SynthFunCmd): return cmd
    elif isinstance(cmd, DefineFunCmd): return DefineFunCmd(cmd.name, cmd.args, cmd.sort, unletTerm(cmd.term))
    elif isinstance(cmd, NopCmd): return cmd
    else: assert False

####

def unletTerm(term, env={}):
    assert isinstance(term, Term)

    if isinstance(term, VarTerm):
        return env[term.name] if term.name in env else term

    elif isinstance(term, FunAppTerm):
        return FunAppTerm(term.funName, tuple(unletTerm(t, env) for t in term.args))

    elif isinstance(term, LetTerm):
        bindings = term.bindings
        bindings = { x: unletTerm(t, env) for x, t in bindings }
        newEnv = env | bindings
        return unletTerm(term.subTerm, newEnv)

    elif isinstance(term, Literal):
        return term

    else: assert False

########################################################################################################################

def containsLetCmd(cmd):
    assert isinstance(cmd, Cmd)
    if isinstance(cmd, DeclareVarCmd): return False
    elif isinstance(cmd, ConstraintCmd): return containsLetTerm(cmd.term)
    elif isinstance(cmd, SynthFunCmd): return False
    elif isinstance(cmd, DefineFunCmd): return containsLetTerm(cmd.term)
    elif isinstance(cmd, NopCmd): return False
    else: assert False

####

def containsLetTerm(term):
    assert isinstance(term, Term)
    if isinstance(term, VarTerm): return False
    elif isinstance(term, FunAppTerm): return any(containsLetTerm(t) for t in term.args)
    elif isinstance(term, LetTerm): return True
    elif isinstance(term, Literal): return False
    else: assert False

########################################################################################################################
# Final Script

if __name__ == '__main__':
    logging.info(f'Hello! (Platform: {platform.python_implementation()} {platform.python_version()})')

    cmdsStr = sys.stdin.read()
    cmds = sygusfmt.deserialize(cmdsStr)

    if any(containsLetCmd(cmd) for cmd in cmds):
        for cmd in cmds:
            print(unletCmd(cmd))
    else: print(cmdsStr, end='') # Preserve original file if no let expressions were found
