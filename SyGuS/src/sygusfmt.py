#!/usr/bin/env python3

########################################################################################################################
# The SyGuS Language Interface: Parsers, Generators, Validators

import base
from sygusast import *
import stdlib

from sexpdata import loads, Symbol

import itertools
import logging
import os
import re

########################################################################################################################
# 1. Deserializing S-expressions

def deserializeFile(filename):
    ans = base.readFile(filename)
    ans = deserialize(ans)
    return ans

def deserialize(s):
    '''Deserializes a string from s-expression notation into nested tuples'''
    s = loads(f'({os.linesep}{s}{os.linesep})', true=None, false=None)

    def unwind(s):
        if isinstance(s, list): return tuple(unwind(s2) for s2 in s)
        elif isinstance(s, Symbol):
            s = s.value()
            if s == 'true': return BoolLit(True)
            elif s == 'false': return BoolLit(False)
            elif re.match(r'#x[0-9A-Fa-f]+', s): return BVLit(value=int(s[2:], base=16), length=4 * (len(s) - 2))
            elif re.match(r'#b[01]+', s): return BVLit(value=int(s[2:], base=2), length=len(s) - 2)
            else: return s
        elif isinstance(s, int): return IntLit(s)
        elif isinstance(s, float): return RealLit(s)
        elif isinstance(s, str): return StringLit(s)
        else: assert False

    def parseSort(sort):
        d = { 'Bool': BoolSort, 'Int': IntSort, 'Real': RealSort, \
              'String': StringSort, 'RegLan': RegLanSort }
        if sort in d: return d[sort]
        elif (len(sort) == 3 and sort[0] == '_' and sort[1] == 'BitVec' and isinstance(sort[2], IntLit)) or \
             (len(sort) == 2 and sort[0] == 'BitVec' and isinstance(sort[1], IntLit)):
            return BVSort(length=sort[-1].value)
        else: raise KeyError(f'Unable to determine sort {sort}')

    def parseTerm(term):
        if isinstance(term, str): return VarTerm(term)
        elif isinstance(term, tuple) and term[0] != 'let':
            funName, *args = term
            args = tuple(parseTerm(t) for t in args)
            return FunAppTerm(funName, args)
        elif isinstance(term, tuple) and term[0] == 'let':
            _, bindings, subTerm = term
            bindings = tuple((b[0], parseTerm(b[-1])) for b in term[1])
            subTerm = parseTerm(subTerm)
            return LetTerm(bindings, subTerm)
        elif isinstance(term, Literal): return term
        else: assert False

    def parseCmd(cmd):
        # logging.info(f'Parsing command {cmd}')
        cmdType = cmd[0].value()
        if cmdType == 'constraint':
            cmd = unwind(cmd)
            _, term = cmd
            return ConstraintCmd(term=parseTerm(term))
        elif cmdType == 'declare-var':
            cmd = unwind(cmd)
            _, name, sort = cmd
            return DeclareVarCmd(name=name, sort=parseSort(sort))
        elif cmdType == 'synth-fun':
            cmd = unwind(cmd)
            assert 4 <= len(cmd) <= 6
            _, name, args, sort = cmd[0:4]
            argSorts = tuple(parseSort(sort) for _, sort in args)
            sort = parseSort(sort)
            return SynthFunCmd(name=name, argSorts=argSorts, sort=sort)
        elif cmdType == 'define-fun':
            cmd = unwind(cmd)
            _, name, args, sort, term = cmd
            args = tuple((name, parseSort(sort)) for name, sort in args)
            return DefineFunCmd(name=name, args=args, sort=parseSort(sort), term=parseTerm(term))
        elif cmdType in NOP_CMDS:
            return NopCmd(raw=cmd)
        elif cmdType in UNSUPPORTED_CMDS:
            raise UnsupportedOperationException(f'No support for SyGuS-IF command {cmd[0]}')
        else: raise KeyError(f'Unknown command {cmd[0]}')

    def parse(s):
        # Eliminate signalling outputs from SyGuS solver
        s = (cmd for cmd in s if cmd != Symbol('unsat'))
        s = (cmd for cmd in s if cmd != Symbol('unknown'))
        s = (cmd for cmd in s if cmd != Symbol('fail'))
        return tuple(parseCmd(cmd) for cmd in s)

    # We don't know how many levels of outermost parentheses are present in the file.
    # If there are outermost parentheses, then the parse function will fail.
    # This code repeatedly removes the outermost layers of parentheses until parsing succeeds.
    # Of course, this is a hack.
    while True:
        try:
            # logging.info(s)
            return parse(s)
        except Exception as e:
            # logging.info(e)
            assert s != s[0]
            s = s[0]
    assert False

########################################################################################################################
# 2. Extract Probe Function From Specification-Implementation Pair

#    When simultaneously synthesizing multiple functions, the implementation will be a list of function definitions,
#    only one of which is of interest. This function substitutes the definitions of all other synthesized functions back
#    into the specification.

#    Turns an instance of a multi-function synthesis problem into an instance of a single-function synthesis problem.

def toSingleSynthFunProblem(spec, impl, holeAddr):
    assert all(isinstance(f, DefineFunCmd) for f in impl)
    for f1 in spec:
        if not isinstance(f1, SynthFunCmd): continue
        assert any(f1.name == f2.name and getArgSorts(f1) == getArgSorts(f2) for f2 in impl), \
               f'Unable to find implementation for synthesis function {f1}'
    for f1 in impl:
        assert any(f1.name == f2.name and getArgSorts(f1) == getArgSorts(f2) \
                   for f2 in spec if isinstance(f2, SynthFunCmd)), \
               f'Could not find synthesis function declaration for implementation function {f1}'

    newImpl = impl[holeAddr[0]]
    newHoleAddr = holeAddr[1:]

    passedProbeFun = False
    newSpec = ()
    for cmd in spec:
        if isinstance(cmd, SynthFunCmd):
            if cmd.name == newImpl.name and getArgSorts(cmd) == getArgSorts(newImpl):
                assert not passedProbeFun
                passedProbeFun = True
                newSpec = newSpec + (cmd,)
            else:
                cmdImpls = tuple(cmdImpl for cmdImpl in impl \
                                 if cmd.name == cmdImpl.name and getArgSorts(cmd) == getArgSorts(cmdImpl))
                assert len(cmdImpls) == 1
                newSpec = newSpec + (cmdImpls[0],)
        else:
            newSpec = newSpec + (cmd,)
    assert passedProbeFun

    assert isinstance(newImpl, DefineFunCmd)
    return (newSpec, newImpl, newHoleAddr)

########################################################################################################################
# 3. Insert probe function at location of hole

def insertProbeFun(spec, impl, holeAddr):
    '''Inserts probe function at location of hole. The probe function is declared using a new SynthFunCmd. The stubbed
       implementation retains the form of a DefineFunCmd. Inserts stubbed implementation and probe function declaration
       back into the spec. This object is the first version of the trivial subspecification.

       Returns a triple, consisting of the trivial subspec, probe function declaration, and stubbed implementation.'''

    ####
    # a. Determine subterm presently at hole

    assert isinstance(impl, DefineFunCmd)
    assert holeAddr[0] == 4

    def findSubtermAtHole(term, holeAddr):
        assert isinstance(term, Term)
        if not holeAddr: return term
        else:
            assert holeAddr[0] > 0
            assert isinstance(term, FunAppTerm)
            return findSubtermAtHole(term.args[holeAddr[0] - 1], holeAddr[1:])

    subtermAtHole = findSubtermAtHole(impl.term, holeAddr[1:])
    logging.info(f'Subterm presently at hole: {subtermAtHole}')

    ####
    # b. Determine sort of hole

    env = { (cmd.name, getArgSorts(cmd)): cmd.sort for cmd in spec if isinstance(cmd, DefineFunCmd) } | \
          { (varName, None): sort for varName, sort in impl.args }

    holeSort = getSort(subtermAtHole, env)
    assert holeSort
    implArgSorts = tuple(sort for _, sort in impl.args)

    ####
    # c. Determine hole name

    possibleProbeNames = (f'h{i}' for i in itertools.count(0))
    possibleProbeNames = (h for h in possibleProbeNames if not stdlib.resolve(h, implArgSorts))
    possibleProbeNames = (h for h in possibleProbeNames \
                            if all(not isinstance(cmd, DeclareVarCmd) or cmd.name != h for cmd in spec))
    possibleProbeNames = (h for h in possibleProbeNames \
                            if all(not isinstance(cmd, SynthFunCmd) or cmd.name != h for cmd in spec))
    possibleProbeNames = (h for h in possibleProbeNames \
                            if all(not isinstance(cmd, DefineFunCmd) or cmd.name != h for cmd in spec))
    probeName = next(possibleProbeNames)

    probeFunDecl = SynthFunCmd(name=probeName, argSorts=implArgSorts, sort=holeSort)

    # logging.info(f'Probe function: {probeFunDecl}')

    ####
    # d. Replace subterm at hole with call to probe function

    def replaceHoleWithProbeCall(e, holeAddr):
        assert isinstance(e, Term)

        if not holeAddr:
            holeArgs = tuple(VarTerm(v) for v, _ in impl.args)
            return FunAppTerm(funName=probeName, args=holeArgs)

        else:
            assert isinstance(e, FunAppTerm)
            assert holeAddr[0] > 0

            newArgs = tuple(arg if i + 1 != holeAddr[0] else replaceHoleWithProbeCall(arg, holeAddr[1:]) \
                            for i, arg in enumerate(e.args))

            return FunAppTerm(funName=e.funName, args=newArgs)

    stubbedImpl = replaceHoleWithProbeCall(impl.term, holeAddr[1:])
    stubbedImpl = DefineFunCmd(name=impl.name, args=impl.args, sort=impl.sort, term=stubbedImpl)
    # logging.info(f'Stubbed implementation: {stubbedImpl}')

    ####

    def transformCmd(cmd):
        if isinstance(cmd, SynthFunCmd):
            yield probeFunDecl
            yield stubbedImpl
        else:
            yield cmd
    subspec = tuple(newCmd for cmd in spec for newCmd in transformCmd(cmd))

    # logging.info('Trivial subspecification:' + os.linesep + \
    #              os.linesep.join(f'    {cmd}' for cmd in subspec))

    return subspec, probeFunDecl, stubbedImpl

########################################################################################################################
# 4. Compute Sorts of Terms

def getSort(term, env):
    '''Finds the sort of a term in the given environment'''

    # logging.info(f'Getting the sort of term {term}')
    assert isinstance(term, Term)

    if isinstance(term, VarTerm):
        if (term.name, None) in env: ans = env[(term.name, None)]
        else:
            logging.warn(f'Unable to resolve variable {term}')
            ans = None

    elif isinstance(term, FunAppTerm):
        argSorts = tuple(getSort(arg, env) for arg in term.args)
        if (term.funName, argSorts) in env: ans = env[(term.funName, argSorts)]
        else:
            ans = stdlib.resolve(term.funName, argSorts)
            if not ans:
                argSortsStr = (str(argSort) for argSort in argSorts)
                argSortsStr = ', '.join(argSortsStr)
                logging.warn(f'Unable to resolve term {term.funName}({argSortsStr})')

    elif isinstance(term, LetTerm):
        newEnv = env | { v: getSort(e, env) for v, e in term.bindings }
        ans = getSort(term.subTerm, newEnv)

    elif isinstance(term, Literal):
        ans = term.sort()

    # logging.info(f'Getting the sort of term {term} ==> {ans}')
    return ans

########################################################################################################################
# 5. Unroll macros

def substituteVars(term, varTermMap):
    # logging.info(f'Substituting {varTermMap} into term {term}')
    assert isinstance(term, Term), f'{term}'

    if isinstance(term, VarTerm): ans = varTermMap[term.name]

    elif isinstance(term, FunAppTerm):
        newArgs = tuple(substituteVars(arg, varTermMap) for arg in term.args)
        ans = FunAppTerm(term.funName, newArgs)

    elif isinstance(term, LetTerm): assert False

    elif isinstance(term, Literal): ans = term

    else: assert False

    # logging.info(f'Substituting {varTermMap} into term {term} ==> {ans}')
    return ans

def unrollMacros(spec):
    # logging.info('Unrolling macros!')

    assert all(isinstance(cmd, Cmd) for cmd in spec)
    assert len(tuple(cmd for cmd in spec if isinstance(cmd, SynthFunCmd))) == 1

    universalVars = dict() # dict[(str, None), Sort]
    macros = dict() # dict[(str, tuple[Sort]), DefineFunCmd]
    synthesisTarget = None

    def unrollTerm(term, env):
        # Returns the unrolled term and its sort

        # logging.info(f'Unrolling macros in term {term} ({type(term)})')
        assert isinstance(term, Term)

        if isinstance(term, VarTerm):
            if (term.name, None) in env: sort = env[(term.name, None)]
            elif (term.name, ()) in macros:
                macro = macros[(term.name, ())]
                term, sort = macro.term, macro.sort
            else:
                logging.warn(f'Unable to resolve variable {term}')
                sort = None
            ans = (term, sort)

        elif isinstance(term, FunAppTerm):
            unrolledArgs = tuple(unrollTerm(arg, env) for arg in term.args)

            argSorts = tuple(sort for _, sort in unrolledArgs)
            unrolledArgs = tuple(arg for arg, _ in unrolledArgs)

            if (term.funName, argSorts) in macros:
                macro = macros[(term.funName, argSorts)]
                varTermMap = zip(macro.args, unrolledArgs)
                varTermMap = { argName: term for ((argName, sort), term) in varTermMap }

                newTerm = substituteVars(macro.term, varTermMap)
                outSort = macro.sort
                ans = (newTerm, outSort)

            elif synthesisTarget and \
                 synthesisTarget.name == term.funName and synthesisTarget.argSorts == argSorts:
                newTerm = FunAppTerm(term.funName, unrolledArgs)
                outSort = synthesisTarget.sort
                ans = (newTerm, outSort)

            else:
                newTerm = FunAppTerm(term.funName, unrolledArgs)
                outSort = stdlib.resolve(term.funName, argSorts)
                if not outSort:
                    argSortsStr = (str(arg) for arg in argSorts)
                    argSortsStr = ', '.join(argSortsStr)
                    logging.warn(f'Unable to resolve function {term.funName}({argSortsStr}) in term {term}')
                ans = (newTerm, outSort)

        elif isinstance(term, LetTerm):
            assert False

        elif isinstance(term, Literal):
            ans = (term, term.sort())

        else: assert False

        # logging.info(f'Unrolling macros in term {term} ==> {ans[0]}')
        return ans

    def unrollCmd(cmd):
        nonlocal universalVars, macros, synthesisTarget
        # logging.info(f'Unrolling macros in command {cmd}')

        if isinstance(cmd, DeclareVarCmd):
            universalVars[(cmd.name, None)] = cmd.sort
            ans = cmd

        elif isinstance(cmd, ConstraintCmd):
            newTerm, sort = unrollTerm(cmd.term, universalVars)
            assert sort == BoolSort
            ans = ConstraintCmd(newTerm)

        elif isinstance(cmd, SynthFunCmd):
            assert not synthesisTarget
            synthesisTarget = cmd
            ans = cmd

        elif isinstance(cmd, DefineFunCmd):
            localVars = { (argName, None): sort for argName, sort in cmd.args }
            newTerm, sort = unrollTerm(cmd.term, localVars)
            assert sort == cmd.sort
            newDefn = DefineFunCmd(cmd.name, cmd.args, cmd.sort, newTerm)

            argSorts = tuple(sort for _, sort in cmd.args)

            macros[(cmd.name, argSorts)] = newDefn
            ans = newDefn

        elif isinstance(cmd, NopCmd):
            ans = cmd

        else: assert False

        # logging.info(f'Unrolling macros in command {cmd} ==> {ans}')
        return ans

    ans = tuple(unrollCmd(cmd) for cmd in spec)
    ans = tuple(cmd for cmd in ans if not isinstance(cmd, DefineFunCmd))
    # logging.info(f'Finished unrolling macros!')
    return ans
