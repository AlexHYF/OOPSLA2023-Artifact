#!/usr/bin/env python3

########################################################################################################################
# Converting to and from indicator representations

import base
import stdlib
from sygusast import *
import sygusfmt
import unletter

import itertools
import logging
import os
import subprocess
import tempfile
import time

########################################################################################################################
# 1. Simplifying indicator records

def simplifySpec(indicatorRec, deadline):

    ####
    # 1. Unpack indicator manufacture record

    universalVars = indicatorRec.universalVars
    indicatorVars = indicatorRec.indicatorVars
    indCallMap = indicatorRec.indCallMap
    functionalConstraint = indicatorRec.functionalConstraint
    indicatorTerms = indicatorRec.indicatorTerms

    ####
    # 2. Universally quantified variables in subsequent SyGuS calls

    env = universalVars | indicatorVars
    declVarCmds = tuple(DeclareVarCmd(name, sort) for ((name, _), sort) in env.items())

    ####
    # 3. Name of target function in subsequent SyGuS calls

    # We will reuse the target name through the simplification process.
    # On the other hand, depending on the subterm being simplified, the sort of the target function may change.
    # We therefore hold off on constructing the SynthFunCmd and FunAppTerm values.

    possibleTargetNames = (f'f{i}' for i in itertools.count(0))
    possibleTargetNames = (fi for fi in possibleTargetNames if (fi, None) not in universalVars)
    possibleTargetNames = (fi for fi in possibleTargetNames if (fi, None) not in indicatorVars)
    possibleTargetNames = (fi for fi in possibleTargetNames if not stdlib.resolve(fi, None))
    possibleTargetNames = (fi for fi in possibleTargetNames if not stdlib.resolve(fi, ()))
    targetName = next(possibleTargetNames)

    ####

    assumptions = functionalConstraint

    newIndicatorTerms = []

    remainingIndicatorTerms = list(indicatorTerms)
    while remainingIndicatorTerms:
        indTerm = remainingIndicatorTerms[0]

        remainingWork = sum(indTerm.size for indTerm in remainingIndicatorTerms)
        thisDeadline = time.time() + indTerm.size * (deadline - time.time()) / remainingWork

        remainingIndicatorTerms.pop(0)

        newIndTerm = simplify(env, declVarCmds, assumptions, indTerm, targetName, thisDeadline)
        if newIndTerm == BoolLit(True): continue
        elif newIndTerm == BoolLit(False):
            logging.info('Inconsistent subspec!')
            newIndicatorTerms = [ newIndTerm ]
            break
        else:
            newIndicatorTerms.append(newIndTerm)
            if base.ENVIRONMENT['accAssumes']:
                assumptions = stdlib.stdAnd(assumptions, newIndTerm)

    if not newIndicatorTerms:
        logging.info('Unconstrained hole!')

    newIndicatorTerms = tuple(newIndicatorTerms)
    logging.info('Simplified indicator terms:')
    for newIndTerm in newIndicatorTerms:
        logging.info(f'    {newIndTerm}')

    ####

    return indicatorRec._replace(indicatorTerms=newIndicatorTerms)

########################################################################################################################

def simplify(env, declVarCmds, assumptions, indTerm, targetName, deadline):
    # logging.info(f'Simplifying indicator term {indTerm}')
    assert isinstance(indTerm, Term)
    targetArgSorts = tuple(declVarCmd.sort for declVarCmd in declVarCmds)

    def simplify2(assumptions, term, deadline):
        # logging.info(f'Simplifying term {term}')
        assert isinstance(term, Term)

        if isinstance(term, VarTerm): ans = term

        elif isinstance(term, FunAppTerm):

            if term.funName == 'ite':
                tc, tt, te = term.args

                dc = time.time() + tc.size * (deadline - time.time()) / term.size
                tc = simplify2(assumptions, tc, dc)
                dt = time.time() + tt.size * (deadline - time.time()) / term.size
                tt = simplify2(stdlib.stdAnd(assumptions, tc), tt, dt)
                de = time.time() + te.size * (deadline - time.time()) / term.size
                te = simplify2(stdlib.stdAnd(assumptions, stdlib.stdNot(tc)), te, de)
                args = (tc, tt, te)
            elif term.funName == 'and':
                tl, tr = term.args

                dl = time.time() + tl.size * (deadline - time.time()) / term.size
                tl = simplify2(assumptions, tl, dl)
                dr = time.time() + tr.size * (deadline - time.time()) / term.size
                tr = simplify2(stdlib.stdAnd(assumptions, tl), tr, dr)
                args = (tl, tr)
            elif term.funName == 'or':
                tl, tr = term.args

                dl = time.time() + tl.size * (deadline - time.time()) / term.size
                tl = simplify2(assumptions, tl, dl)
                dr = time.time() + tr.size * (deadline - time.time()) / term.size
                tr = simplify2(stdlib.stdAnd(assumptions, stdlib.stdNot(tl)), tr, dr)
                args = (tl, tr)
            else:
                oldArgs = term.args
                newArgs = ()
                while oldArgs:
                    remainingWork = sum(arg.size for arg in oldArgs)
                    argDeadline = time.time() + oldArgs[0].size * (deadline - time.time()) / remainingWork

                    newArgs = newArgs + (simplify2(assumptions, oldArgs[0], argDeadline),)
                    oldArgs = oldArgs[1:]
                args = newArgs

            ans = FunAppTerm(term.funName, args)

            targetSort = sygusfmt.getSort(ans, env)
            targetDecl = SynthFunCmd(name=targetName, argSorts=targetArgSorts, sort=targetSort)
            targetCall = FunAppTerm(targetName, tuple(VarTerm(declVarCmd.name) for declVarCmd in declVarCmds))

            constraint = stdlib.stdImplies(assumptions, stdlib.stdEq(targetCall, ans))
            # logging.info(f'{constraint}')

            spec = (NopCmd(raw='(set-logic ALL)'), targetDecl) + declVarCmds + \
                   (ConstraintCmd(constraint), NopCmd(raw='(check-synth)'))
            targetDefn = callSygus(spec, deadline)
            if targetDefn:
                assert isinstance(targetDefn, DefineFunCmd)
                varTermMap = { arg: VarTerm(cmd.name) for ((arg, _), cmd) in zip(targetDefn.args, declVarCmds) }
                ans = sygusfmt.substituteVars(targetDefn.term, varTermMap)
                ans = stdlib.pevalTerm(ans)
                if term.size < ans.size: ans = term

            else:
                ans = term

        elif isinstance(term, LetTerm): assert False

        elif isinstance(term, Literal): ans = term

        # logging.info(f'Simplifying term {term} ({term.size}) ==> {ans} ({ans.size})')
        return ans

    ans = simplify2(assumptions, indTerm, deadline)
    # logging.info(f'Simplifying indicator term {indTerm} ==> {ans}')
    return ans

########################################################################################################################

def callSygus(spec, deadline):
    # TODO: Handle timeouts and stuff

    baseDir = os.path.realpath(__file__)
    baseDir = os.path.dirname(baseDir)
    solvers = { \
        'cvc5': (f'{baseDir}/../solvers/cvc5/build/bin/cvc4', '--lang=sygus1'),
        'eusolver': (f'{baseDir}/../solvers/eusolver/eusolver',)
    }
    solver = solvers[base.ENVIRONMENT['solver']]


    with tempfile.NamedTemporaryFile(mode='w+t', suffix='.sl') as specFile:
        # logging.info(f'Writing specification to {specFile.name}')
        for cmd in spec: print(f'{cmd}', file=specFile)
        specFile.flush()

        timeout = deadline - time.time()
        try:
            solverProc = subprocess.run(solver + (specFile.name,), capture_output=True, text=True, timeout=timeout)
            impl = sygusfmt.deserialize(solverProc.stdout)
        except subprocess.TimeoutExpired:
            logging.info(f'Timeout: {timeout}')
            impl = None

        if impl:
            impl, = impl
            impl = unletter.unletCmd(impl)
            assert isinstance(impl, DefineFunCmd)
        else:
            impl = None
        return impl
