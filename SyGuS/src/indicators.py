#!/usr/bin/env python3

########################################################################################################################
# Converting to and from indicator representations

import stdlib
from sygusast import *
import sygusfmt

from collections import namedtuple
import itertools
import logging

########################################################################################################################
# 1. Converting subspecification into indicator functions

MakeRecord = namedtuple('MakeType', ('universalVars', 'indicatorVars', 'indCallMap', \
                                     'functionalConstraint', \
                                     'indicatorTerms'))

def make(subspec, probeFunDecl):

    ####
    # a. Find environment in which constraint is evaluated and collect constraints

    universalVars = { (cmd.name, None): cmd.sort for cmd in subspec if isinstance(cmd, DeclareVarCmd) }
    constraintEnv = universalVars | { (probeFunDecl.name, probeFunDecl.argSorts): probeFunDecl.sort }
    constraints = tuple(cmd for cmd in subspec if isinstance(cmd, ConstraintCmd))

    ####
    # b. Identify all syntactically distinct calls to the probe function

    def collectSynthFunCalls(term):
        assert isinstance(term, Term)
        if isinstance(term, VarTerm): ans = frozenset()
        elif isinstance(term, FunAppTerm):
            ans = frozenset(call for arg in term.args for call in collectSynthFunCalls(arg))
            argSorts = tuple(sygusfmt.getSort(arg, constraintEnv) for arg in term.args)
            if term.funName == probeFunDecl.name and argSorts == probeFunDecl.argSorts:
                ans = ans | frozenset((term,))
        elif isinstance(term, LetTerm): assert False
        elif isinstance(term, Literal): ans = frozenset()
        else: assert False
        return ans

    synthFunCalls = frozenset(call for c in constraints for call in collectSynthFunCalls(c.term))
    logging.info(f'Calls to probe function ({len(synthFunCalls)}):')
    for call in synthFunCalls:
        logging.info(f'    {call}')

    ####
    # c. Associate each syntactically distinct call to the probe function with an indicator variable

    indCallMap = {} # : dict[str, Term]
    callIndMap = {} # : dict[Term, VarTerm]

    possibleNameCounter = 0
    for call in synthFunCalls:
        while True:
            nextPossibleName = f'ind{possibleNameCounter}'
            if (nextPossibleName, None) in universalVars or \
               nextPossibleName == probeFunDecl.name or \
               stdlib.resolve(nextPossibleName, None) or \
               stdlib.resolve(nextPossibleName, ()) or \
               nextPossibleName in indCallMap:
                possibleNameCounter = possibleNameCounter + 1
                continue
            break
        vCall = nextPossibleName
        indCallMap[vCall] = call
        callIndMap[call] = VarTerm(vCall)

    indicatorVars = { (vCall, None): probeFunDecl.sort for vCall in indCallMap.keys() }

    for call, vCall in callIndMap.items():
        logging.info(f'{call}: {vCall}')

    ####
    # d. Rewrite constraint to reference indicator variables

    def make2(term):
        assert isinstance(term, Term)
        if isinstance(term, VarTerm): ans = term
        elif isinstance(term, FunAppTerm) and term in callIndMap: ans = callIndMap[term]
        elif isinstance(term, FunAppTerm):
            args = tuple(make2(arg) for arg in term.args)
            ans = FunAppTerm(term.funName, args)
        elif isinstance(term, LetTerm): assert False
        elif isinstance(term, Literal): ans = term
        else: assert False
        return ans

    indicatorTerms = tuple(make2(c.term) for c in constraints)
    logging.info('Printing indicator terms:')
    for indTerm in indicatorTerms:
        logging.info(f'    {indTerm}')

    ####
    # e. Collect functional constraints

    def getFunctionalConstraint(call1, call2):
        assert isinstance(call1, FunAppTerm)
        assert isinstance(call2, FunAppTerm)
        assert call1.funName == probeFunDecl.name and len(call1.args) == len(probeFunDecl.argSorts)
        assert call2.funName == probeFunDecl.name and len(call2.args) == len(probeFunDecl.argSorts)

        l = None
        for arg1, arg2 in zip(call1.args, call2.args):
            e = stdlib.stdEq(make2(arg1), make2(arg2))
            e = stdlib.pevalTerm(e)
            if e == BoolLit(False):
                l = e
                break
            elif e != BoolLit(True):
                l = stdlib.stdAnd(l, e) if l else e
                l = stdlib.pevalTerm(e)
        if not l: l = BoolLit(True)

        if l == BoolLit(False):
            ans = BoolLit(True)
        else:
            ind1 = callIndMap[call1]
            ind2 = callIndMap[call2]
            r = stdlib.stdEq(ind1, ind2)

            if l == BoolLit(True):
                ans = r
            else:
                ans = stdlib.stdImplies(l, r)
                ans = stdlib.pevalTerm(ans)

        return ans

    sfcList = list(synthFunCalls)
    fcs = (getFunctionalConstraint(sfcList[i], sfcList[j]) for i in range(len(sfcList)) \
                                                           for j in range(i + 1, len(sfcList)))
    functionalConstraint = None
    for fc in fcs:
        if fc != BoolLit(True):
            logging.info(f'    {fc}')
            functionalConstraint = stdlib.stdAnd(functionalConstraint, fc) if functionalConstraint else fc
            functionalConstraint = stdlib.pevalTerm(functionalConstraint)
    if not functionalConstraint: functionalConstraint = BoolLit(True)
    logging.info(f'Functional constraint: {functionalConstraint}')

    ####

    return MakeRecord(universalVars=universalVars, indicatorVars=indicatorVars, indCallMap=indCallMap, \
                      functionalConstraint=functionalConstraint, \
                      indicatorTerms=indicatorTerms)

########################################################################################################################
# 2. Recovering specifications from indicator functions

def recoverSpec(probeFunDecl, indicatorMfgRecord):
    universalVars = indicatorMfgRecord.universalVars
    indicatorVars = indicatorMfgRecord.indicatorVars
    indCallMap = indicatorMfgRecord.indCallMap
    functionalConstraint = indicatorMfgRecord.functionalConstraint
    indicatorTerms = indicatorMfgRecord.indicatorTerms

    ####

    ans = (probeFunDecl,) + tuple(DeclareVarCmd(v, sort) for ((v, _), sort) in universalVars.items())
    indSubstMap = indCallMap | { v: VarTerm(v) for (v, _) in universalVars.keys() }
    for indTerm in indicatorTerms:
        constraintTerm = sygusfmt.substituteVars(indTerm, indSubstMap)
        ans = ans + (ConstraintCmd(constraintTerm),)
    ans = ans + (NopCmd('(check-synth)'),)

    ####

    return ans
