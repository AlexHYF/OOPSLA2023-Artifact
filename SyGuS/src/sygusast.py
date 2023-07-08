#!/usr/bin/env python3

########################################################################################################################
# SyGuS Abstract Syntax Trees

from sexpdata import dumps

from dataclasses import dataclass
import logging

########################################################################################################################
# 1. Sorts

@dataclass(order=True, frozen=True)
class Sort:
    name: str
    def __str__(self):
        return self.name

BoolSort = Sort('Bool')
IntSort = Sort('Int')
RealSort = Sort('Real')
StringSort = Sort('String')
RegLanSort = Sort('RegLan')

@dataclass(init=False, order=True, frozen=True)
class BVSort(Sort):
    length: int
    def __init__(self, length):
        super().__init__('BV')
        assert 0 < length
        object.__setattr__(self, 'length', length)
    def __str__(self):
        return f'(BitVec {self.length})'

########################################################################################################################
# 2. Terms and Literals

@dataclass(init=False, order=True, frozen=True)
class Term:
    size: int
    def __init__(self, size):
        assert 0 < size
        object.__setattr__(self, 'size', size)

####
# Terms

@dataclass(init=False, order=True, frozen=True)
class VarTerm(Term):
    name: str
    def __init__(self, name):
        super().__init__(1)
        object.__setattr__(self, 'name', name)
    def __str__(self):
        return self.name

@dataclass(init=False, order=True, frozen=True)
class FunAppTerm(Term):
    funName: str
    args: tuple[Term]
    def __init__(self, funName, args):
        super().__init__(1 + sum(arg.size for arg in args))
        object.__setattr__(self, 'funName', funName)
        object.__setattr__(self, 'args', args)
    def __str__(self):
        ans = (str(arg) for arg in self.args)
        ans = ' '.join(ans)
        ans = f'({self.funName} {ans})'
        return ans

@dataclass(init=False, order=True, frozen=True)
class LetTerm(Term):
    bindings: tuple[tuple[str, Term]]
    subTerm: Term
    def __init__(self, bindings, subTerm):
        super().__init__(1 + sum(t.size for _, t in bindings) + subTerm.size)
        object.__setattr__(self, 'bindings', bindings)
        object.__setattr__(self, 'subTerm', subTerm)
    def __str__(self):
        bindingsStr = (f'({v} {e})' for v, e in self.bindings)
        bindingsStr = ' '.join(bindingsStr)
        bindingsStr = f'({bindingsStr})'
        return f'(let {bindingsStr} {self.subTerm})'

####
# Literals

@dataclass(init=False, order=True, frozen=True)
class Literal(Term):
    value: 'Value'
    def __init__(self, value):
        super().__init__(1)
        object.__setattr__(self, 'value', value)

@dataclass(init=False, order=True, frozen=True)
class BoolLit(Literal):
    def __init__(self, value):
        super().__init__(value)
        assert isinstance(value, bool)
    def __str__(self):
        return 'true' if self.value else 'false'
    def sort(self):
        return BoolSort

@dataclass(init=False, order=True, frozen=True)
class IntLit(Literal):
    def __init__(self, value):
        super().__init__(value)
        assert isinstance(value, int)
    def __str__(self):
        return str(self.value)
    def sort(self):
        return IntSort

@dataclass(init=False, order=True, frozen=True)
class RealLit(Literal):
    def __init__(self, value):
        super().__init__(value)
    def __str__(self):
        return str(self.value)
    def sort(self):
        return RealSort

@dataclass(init=False, order=True, frozen=True)
class BVLit(Literal):
    length: int

    def __init__(self, value, length):
        super().__init__(value)
        assert 0 <= value
        assert value < (1 << length)
        assert 0 < length
        object.__setattr__(self, 'length', length)

    def __str__(self):
        formatter, padLen, formatSpec = (hex, self.length / 4, '#x') if self.length % 4 == 0 else \
                                        (bin, self.length, '#b')
        ans = formatter(self.value)
        ans = ans[2:].upper()
        ans = ans.rjust(int(padLen), '0')
        ans = f'{formatSpec}{ans}'
        return ans

    def sort(self):
        return BVSort(self.length)

@dataclass(init=False, order=True, frozen=True)
class StringLit(Literal):
    def __init__(self, value):
        super().__init__(value)
        assert isinstance(value, str)
    def __str__(self):
        return f'"{self.value}"'

    def sort(self):
        return StringSort

########################################################################################################################
# 3. Commands

@dataclass(order=True, frozen=True)
class Cmd:
    pass

@dataclass(order=True, frozen=True)
class DeclareVarCmd(Cmd):
    name: str
    sort: Sort
    def __str__(self):
        return f'(declare-var {self.name} {self.sort})'

@dataclass(order=True, frozen=True)
class ConstraintCmd(Cmd):
    term: Term
    def __str__(self):
        return f'(constraint {self.term})'

# The final argument SynthFun.raw encodes the raw s-expression corresponding to SynthFunCmd.
# Necessary since we are not unpacking grammars.
@dataclass(order=True, frozen=True)
class SynthFunCmd(Cmd):
    name: str
    argSorts: tuple[Sort]
    sort: Sort
    # raw: 'Raw s-expression, "(synth-fun {name} ...)"'
    def __str__(self):
        # if self.raw: return self.raw
        argSortsStr = (f'(v{i} {T})' for i, T in enumerate(self.argSorts))
        argSortsStr = ' '.join(argSortsStr)
        argSortsStr = f'({argSortsStr})'
        return f'(synth-fun {self.name} {argSortsStr} {self.sort})'

@dataclass(order=True, frozen=True)
class DefineFunCmd(Cmd):
    name: str
    args: tuple[(str, Sort)]
    sort: Sort
    term: Term
    def __str__(self):
        argsStr = (f'({v} {T})' for v, T in self.args)
        argsStr = ' '.join(argsStr)
        argsStr = f'({argsStr})'
        return f'(define-fun {self.name} {argsStr} {self.sort} {self.term})'

####

NOP_CMDS = frozenset({ 'set-logic', 'check-synth', 'set-options', 'set-option' })

@dataclass(order=True, frozen=True)
class NopCmd(Cmd):
    raw: 'Raw s-expression'
    def __str__(self):
        return dumps(self.raw, str_as='symbol')

####

UNSUPPORTED_CMDS = frozenset({ \
    'assume', \
    \
    'chc-constraint', 'declare-weight', 'inv-constraint', 'optimize-synth', 'set-feature' \
    \
    'oracle-assume', 'oracle-constraint', 'declare-oracle-fun', 'oracle-constraint-io', \
    'oracle-constraint-cex', 'oracle-constraint-membership', 'oracle-constraint-poswitness', \
    'oracle-constraint-negwitness', 'declare-correctness-oracle', \
    'declare-correctness-cex-oracle', \
    \
    'declare-datatype', 'declare-datatypes', 'declare-sort', 'define-sort', 'set-info' \
})

####
# Helper Functions

def getArgSorts(cmd):
    if isinstance(cmd, SynthFunCmd): return cmd.argSorts
    elif isinstance(cmd, DefineFunCmd): return tuple(T for _, T in cmd.args)
    else: assert False

def cmdSeqSize(cmds):
    s1 = sum(cmd.term.size for cmd in cmds if isinstance(cmd, ConstraintCmd))
    s2 = max(0, len(tuple(cmd for cmd in cmds if isinstance(cmd, ConstraintCmd))) - 1)
    s3 = sum(cmd.term.size for cmd in cmds if isinstance(cmd, DefineFunCmd))
    return s1 + s2 + s3
