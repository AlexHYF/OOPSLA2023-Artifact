#!/usr/bin/env python3

########################################################################################################################
# Main entry point: Invokes the algorithm that constructs subspecifications.

# Usage:
# source venv/bin/activate
# ./main.py spec.sl impl.sl

# 1. spec.sl: File containing the specification
# 2. impl.sl: File containing the implementation

# Accepts a sequence of hole addresses (separated by -1), and prints the constructed subspecifications to stdout.
# Set the TIMEOUT and SOLVER environment variables to set the per-hole timeout and backend SyGuS solver respectively.
# See base.ENVIRONMENT for details.

########################################################################################################################
# 1. Preamble

import base
import indicators
import simplifier
import stdlib
from sygusast import *
import sygusfmt
import unletter

# import indicators
# import Reformation

import os
import time
import logging
import sys

####

logging.info(f'Hello!')

####

specFilename, implFilename = sys.argv[1:]
logging.info(f'specFilename: {specFilename}')
logging.info(f'implFilename: {implFilename}')
base.printEnvironment(logging.info)

####

spec = sygusfmt.deserializeFile(specFilename)
# logging.info('Specification:' + os.linesep + \
#              os.linesep.join(f'    {cmd}' for cmd in spec))

impl = sygusfmt.deserializeFile(implFilename)
# logging.info('Implementation:' + os.linesep + \
#              os.linesep.join(f'    {cmd}' for cmd in impl))

assert all(not unletter.containsLetCmd(cmd) for cmd in spec)
assert all(not unletter.containsLetCmd(cmd) for cmd in impl)

origSpecSize = cmdSeqSize(spec)
logging.info(f'Specification size: {origSpecSize}')
origImplSize = cmdSeqSize(impl)
logging.info(f'Implementation size: {origImplSize}')

########################################################################################################################

def processHole(spec, impl, holeAddr):
    startTime = time.time()
    deadline = startTime + base.ENVIRONMENT['perHoleTimeout']

    logging.info('----------------')
    logging.info(f'holeAddr: {holeAddr}')

    origHoleAddr = holeAddr
    spec, impl, holeAddr = sygusfmt.toSingleSynthFunProblem(spec, impl, holeAddr)
    assert len(tuple(cmd for cmd in spec if isinstance(cmd, SynthFunCmd))) == 1
    assert isinstance(impl, sygusfmt.DefineFunCmd)

    subspec, probeFunDecl, stubbedImpl = sygusfmt.insertProbeFun(spec, impl, holeAddr)
    subspecSize1 = max(cmdSeqSize(subspec), 1)
    subspecTime1 = time.time() - startTime

    logging.info('Probe function:' + os.linesep + f'    {probeFunDecl}')
    logging.info('Stubbed implementation:' + os.linesep + f'    {stubbedImpl}')
    # logging.info('Trivial subspecification:' + os.linesep + \
    #              os.linesep.join(f'    {cmd}' for cmd in subspec))

    subspec = sygusfmt.unrollMacros(subspec)
    subspecSize2 = max(cmdSeqSize(subspec), 1)
    subspecTime2 = time.time() - startTime

    # logging.info('Trivial subspecification (Unrolled):' + os.linesep + \
    #              os.linesep.join(f'    {cmd}' for cmd in subspec))

    ####

    subspec = tuple(stdlib.pevalCmd(cmd) for cmd in subspec)
    subspec = tuple(cmd for cmd in subspec if not isinstance(cmd, ConstraintCmd) or cmd.term != BoolLit(True))
    subspecSize3 = max(cmdSeqSize(subspec), 1)
    subspecTime3 = time.time() - startTime

    logging.info('Subspec (After partial evaluation):' + os.linesep + \
                 os.linesep.join(f'    {cmd}' for cmd in subspec))

    ####

    indicatorMfgRecord = indicators.make(subspec, probeFunDecl)
    indicatorMfgRecord = simplifier.simplifySpec(indicatorMfgRecord, deadline)
    subspec = indicators.recoverSpec(probeFunDecl, indicatorMfgRecord)
    subspecSize4 = max(cmdSeqSize(subspec), 1)
    subspecTime4 = time.time() - startTime

    ####

    print('----------------')
    print(f'; Hole: {origHoleAddr}')
    for cmd in subspec: print(str(cmd))
    print()

    ####

    holeAddrStr = (str(i) for i in origHoleAddr + (-1,))
    holeAddrStr = ' '.join(holeAddrStr)

    logging.info(f'Hole Summary, {holeAddrStr}, , ' + \
                 f'{origSpecSize}, {origImplSize}, , ' + \
                 f'{subspecSize1}, {subspecTime1}, , ' + \
                 f'{subspecSize2}, {subspecTime2}, , ' + \
                 f'{subspecSize3}, {subspecTime3}, , ' + \
                 f'{subspecSize4}, {subspecTime4}')
    # sys.exit(0)
    base.logTime(f'Hole {origHoleAddr}', time.time() - startTime)
    return

####

for holeAddr in base.holeAddrStream():
    processHole(spec, impl, holeAddr)
