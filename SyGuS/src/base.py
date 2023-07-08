#!/usr/bin/env python3

########################################################################################################################
# Common Setup Procedure

import atexit
from collections import namedtuple
import logging
import os
import platform
import signal
import sys
import time

########################################################################################################################
# 1. Logging

logging.basicConfig(
    level=logging.INFO, \
    format="[%(asctime)s] %(levelname)s [%(module)s.%(funcName)s:%(lineno)d] %(message)s", \
    datefmt="%H:%M:%S")

########################################################################################################################
# 2. Environment Variables

def loadEnvironment():
    accAssumes = bool(os.getenv('ACC_ASSUMES', default=False))

    def procTimeout(t):
        unit = t[-1]
        if unit == 's': t = int(t[:-1])
        elif unit == 'm': t = int(t[:-1]) * 60
        elif unit == 'h': t = int(t[:-1]) * 60 * 60
        elif unit == 'd': t = int(t[:-1]) * 60 * 60 * 24
        else: t = int(t)
        return t
    perHoleTimeout = procTimeout(os.getenv('PER_HOLE_TIMEOUT', default='300s'))

    platformStr = f'{platform.python_implementation()} {platform.python_version()}'
    solver = os.getenv('SOLVER', default='cvc5')

    return { 'accAssumes': accAssumes, 'perHoleTimeout': perHoleTimeout, 'platform': platformStr, 'solver': solver }

ENVIRONMENT = loadEnvironment()

def printEnvironment(printer):
    printer('Environment variables:')
    for k, v in ENVIRONMENT.items():
        printer(f'    {k}: {v}')

########################################################################################################################
# 3. Input Streams

def tokenStream(file=sys.stdin, sep=None):
    '''Tokenizes the contents of file in the manner of cin from the C++ standard library, and returns the stream of
       tokens. The token separator sep is interpreted by the str.split() function.'''
    for line in file:
        for token in line.split(sep=sep):
            yield token

def holeAddrStream(file=sys.stdin, sep=None, holeSep=-1):
    '''Interprets the contents of file as a sequence of hole addresses. The token separator sep is interpreted by the
       str.split() function. Individual hole addresses are separated by holeSep.'''
    nextAddr = []
    for token in tokenStream(file=file, sep=sep):
        def isInt(s):
            try:
                int(s)
                return True
            except:
                return False

        if token == holeSep or (isInt(token) and isInt(holeSep) and int(token) == int(holeSep)):
            yield tuple(nextAddr)
            nextAddr = []
        else:
            token = int(token)
            assert token >= 0
            nextAddr.append(token)
    assert not nextAddr, f'Incomplete address {tuple(nextAddr)} at end of stream'

def readFile(filename):
    with open(filename) as f:
        return f.read()

########################################################################################################################
# 4. Timers

scriptStartTime = time.time()
Timer = namedtuple('Timer', ('numCalls', 'totalTime', 'maxTime'))
timers = {}

def logTime(name, t):
    if name not in timers: timers[name] = Timer(0, 0, 0)
    numCalls, prevTime, prevMax = timers[name]
    timers[name] = Timer(numCalls + 1, prevTime + t, max(prevMax, t))

def getTimer(name):
    if name not in timers: timers[name] = Timer(0, 0, 0)
    return timers[name]

def printTimers():
    logTime('script', time.time() - scriptStartTime)
    logging.info('--- Timers ---')
    for k, (vn, vt, vm) in sorted(timers.items(), key=lambda kv: kv[1].totalTime):
        logging.info(f'{k}: {vt} seconds total, {vn} calls, {vm} seconds max')

atexit.register(printTimers)

########################################################################################################################
# 5. Defining Timeouts
#    https://stackoverflow.com/a/22348885
#    This approach only works for single-threaded programs.

class timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message
    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)
    def __exit__(self, type, value, traceback):
        signal.alarm(0)
