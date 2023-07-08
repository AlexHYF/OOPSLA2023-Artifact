#!/usr/bin/env python3

########################################################################################################################
# The SyGuS Standard Library

from sygusast import *

import math

########################################################################################################################

def resolve(name, argSorts):
    '''Determines the output sort from the name of a function and the sorts of its arguments.
       Returns None if unable to resolve the function.
       See Section 2.2, Section 5.1 and Appendix B of SyGuS-IF V2.1.

       To a first approximation, this should be a map from function name to its sort.

       This is complicated by the fact that equality (= : 'a -> 'a -> Bool), (ite : Bool -> 'a -> 'a -> 'a), and
       bit-vector operations (bvadd : BV n -> BV n -> BV n), bvsub, etc. are polymorphic. In addition, arithmetic
       operators such as (+) are overloaded to either mean ((+) : Int -> Int -> Int) or ((+) : Real -> Real -> Real)
       depending on context.

       As a result, resolving a function requires knowledge of the sorts of its input arguments. In addition, the
       complete mapping is no longer a finite object, thus precluding the use of a standard map data structure for this
       purpose.

       While we're at it, we may as well think of literals as values defined in the standard library with appropriate
       sorts.'''

    if name == '=' and len(argSorts) == 2 and argSorts[0] == argSorts[1]: return BoolSort
    elif name == 'ite' and len(argSorts) == 3 and \
         argSorts[0] == BoolSort and argSorts[1] == argSorts[2]: return argSorts[1]

    if not argSorts:
        if isinstance(name, BoolLit): return BoolSort
        elif isinstance(name, IntLit): return IntSort
        elif isinstance(name, RealLit): return RealSort
        elif isinstance(name, BVLit): return BVSort(len=name.len)
        elif isinstance(name, StringLit): return StringSort

    funs = { ('not', (BoolSort,)): BoolSort \
           , ('and', (BoolSort, BoolSort)): BoolSort \
           , ('or', (BoolSort, BoolSort)): BoolSort \
           , ('=>', (BoolSort, BoolSort)): BoolSort
           , ('xor', (BoolSort, BoolSort)): BoolSort \
           \
           , ('-', (IntSort,)): IntSort \
           , ('+', (IntSort, IntSort)): IntSort \
           , ('-', (IntSort, IntSort)): IntSort \
           , ('*', (IntSort, IntSort)): IntSort \
           , ('div', (IntSort, IntSort)): IntSort \
           , ('mod', (IntSort, IntSort)): IntSort \
           , ('abs', (IntSort,)): IntSort \
           \
           , ('>', (IntSort, IntSort)): BoolSort \
           , ('>=', (IntSort, IntSort)): BoolSort \
           , ('<', (IntSort, IntSort)): BoolSort \
           , ('<=', (IntSort, IntSort)): BoolSort \
           \
           , ('-', (RealSort,)): RealSort \
           , ('+', (RealSort, RealSort)): RealSort \
           , ('-', (RealSort, RealSort)): RealSort \
           , ('*', (RealSort, RealSort)): RealSort \
           , ('/', (RealSort, RealSort)): RealSort \
             # The abs : RealSort -> RealSort function is not required by Appendix B.2
           , ('abs', (RealSort,)): RealSort \
           \
           , ('>', (RealSort, RealSort)): BoolSort \
           , ('>=', (RealSort, RealSort)): BoolSort \
           , ('<', (RealSort, RealSort)): BoolSort \
           , ('<=', (RealSort, RealSort)): BoolSort \
           \
           , ('str.++', (StringSort, StringSort)): StringSort \
           , ('str.at', (StringSort, IntSort)): StringSort \
           , ('str.substr', (StringSort, IntSort, IntSort)): StringSort \
             # There appears to be a mistake in Appendix B.4 with the signature of str.indexof.
             # Cf. https://smtlib.cs.uiowa.edu/theories-UnicodeStrings.shtml
           , ('str.indexof', (StringSort, StringSort, IntSort)): IntSort \
           , ('str.replace', (StringSort, StringSort, StringSort)): StringSort \
           , ('str.from_int', (IntSort,)): StringSort \
           , ('str.from_code', (IntSort,)): StringSort \
           \
           , ('str.to_re', (StringSort,)): RegLanSort \
           , ('re.++', (RegLanSort, RegLanSort)): RegLanSort \
           , ('re.union', (RegLanSort, RegLanSort)): RegLanSort \
           , ('re.inter', (RegLanSort, RegLanSort)): RegLanSort \
           , ('re.*', (RegLanSort,)): RegLanSort \
           , ('re.+', (RegLanSort,)): RegLanSort \
           , ('re.opt', (RegLanSort,)): RegLanSort \
           , ('re.range', (StringSort, StringSort)): RegLanSort \
           \
           , ('str.len', (StringSort,)): IntSort \
           , ('str.to_int', (StringSort,)): IntSort \
           , ('str.to_code', (StringSort,)): IntSort \
           \
           , ('str.in_re', (StringSort, RegLanSort)): BoolSort \
           , ('str.contains', (StringSort, StringSort)): BoolSort \
           , ('str.prefixof', (StringSort, StringSort)): BoolSort \
           , ('str.suffixof', (StringSort, StringSort)): BoolSort \
           , ('str.<', (StringSort, StringSort)): BoolSort \
           , ('str.<=', (StringSort, StringSort)): BoolSort \
           , ('str.is_digit', (StringSort,)): BoolSort \
           }

    if (name, argSorts) in funs: return funs[(name, argSorts)]

    if argSorts and all(T == argSorts[0] for T in argSorts) and isinstance(argSorts[0], BVSort):
        bvn = argSorts[0]
        bvfuns = { ('bvnot', (bvn,)): bvn \
                 , ('bvand', (bvn, bvn)): bvn \
                 , ('bvor', (bvn, bvn)): bvn \
                 , ('bvxor', (bvn,bvn)): bvn \
                 , ('bvneg', (bvn,)): bvn \
                 , ('bvadd', (bvn, bvn)): bvn \
                 , ('bvsub', (bvn, bvn)): bvn \
                 , ('bvmul', (bvn, bvn)): bvn \
                 , ('bvudiv', (bvn, bvn)): bvn \
                 , ('bvurem', (bvn, bvn)): bvn \
                 , ('bvshl', (bvn, bvn)): bvn \
                 , ('bvlshr', (bvn, bvn)): bvn \
                   # Surprisingly, neither SMT-LIB 2.6 nor SyGuS-IF V2.1 speak of bvashr.
                 , ('bvashr', (bvn, bvn)): bvn \
                 }
        if (name, argSorts) in bvfuns: return bvfuns[(name, argSorts)]

    return None # f'Unable to resolve function {name}({argSorts})'

########################################################################################################################
# 2. Standard Functions

def stdEq(t1, t2):
    return FunAppTerm('=', (t1, t2))

def stdAnd(t1, t2):
    return FunAppTerm('and', (t1, t2))

def stdOr(t1, t2):
    return FunAppTerm('or', (t1, t2))

def stdNot(t1):
    return FunAppTerm('not', (t1,))

def stdImplies(t1, t2):
    return FunAppTerm('=>', (t1, t2))

def stdNeg(t1):
    return FunAppTerm('-', (t1,))

def stdAbs(t1):
    return FunAppTerm('abs', (t1,))

def stdConcat(t1, t2):
    return FunAppTerm('str.++', (t1, t2))

def stdBVNot(t1):
    return FunAppTerm('bvnot', (t1,))

def stdBVNeg(t1):
    return FunAppTerm('bvneg', (t1,))

########################################################################################################################

def pevalCmd(cmd):
    '''Partially evaluate commands.'''

    assert isinstance(cmd, Cmd)

    if isinstance(cmd, DeclareVarCmd): ans = cmd
    elif isinstance(cmd, ConstraintCmd): ans = ConstraintCmd(pevalTerm(cmd.term))
    elif isinstance(cmd, SynthFunCmd): ans = cmd
    elif isinstance(cmd, DefineFunCmd): ans = DefineFunCmd(cmd.name, cmd.args, cmd.sort, pevalTerm(cmd.term))
    elif isinstance(cmd, NopCmd): ans = cmd

    return ans

####

def pevalTerm(term):
    '''Partially evaluate terms.'''

    # logging.info(f'Partially evaluating term {term}')
    assert isinstance(term, Term)

    if isinstance(term, VarTerm): ans = term
    elif isinstance(term, FunAppTerm):
        args = tuple(pevalTerm(arg) for arg in term.args)
        term = FunAppTerm(term.funName, args)
        ans = pevalFunApp(term)
    elif isinstance(term, LetTerm): assert False
    elif isinstance(term, Literal): ans = term
    else: assert False

    # logging.info(f'Partially evaluating term {term} ==> {ans}, {type(ans)}')
    return ans

####

def pevalFunApp(term):
    '''Partially evaluate function applications.'''

    assert isinstance(term, FunAppTerm)
    name = term.funName
    args = term.args

    ans = term

    ####
    # Core
    # https://smtlib.cs.uiowa.edu/theories-Core.shtml

    if name == '=' and len(args) == 2:
        lhs, rhs = args
        if isinstance(lhs, Literal) and isinstance(rhs, Literal):
            ans = BoolLit(lhs.value == rhs.value)
        elif lhs == rhs: return BoolLit(True)

    elif name == 'ite' and len(args) == 3:
        cond, thenTerm, elseTerm = args
        if isinstance(cond, BoolLit):
            ans = thenTerm if cond.value else elseTerm
        elif thenTerm == elseTerm:
            ans = thenTerm

    ####
    # Boolean operations

    elif name == 'not' and len(args) == 1:
        operand, = args
        if isinstance(operand, BoolLit):
            ans = BoolLit(not operand.value)
        elif isinstance(operand, FunAppTerm) and operand.funName == 'not' and len(operand.args) == 1:
            ans, = operand.args

    elif name == 'and' and len(args) == 2:
        l, r = args
        if isinstance(l, BoolLit):
            ans = r if l.value else l
        elif isinstance(r, BoolLit):
            ans = l if r.value else r
        elif l == r:
            ans = l

    elif name == 'or' and len(args) == 2:
        l, r = args
        if isinstance(l, BoolLit):
            ans = l if l.value else r
        elif isinstance(r, BoolLit):
            ans = r if r.value else l
        elif l == r:
            ans = l

    elif name == '=>' and len(args) == 2:
        l, r = args
        if isinstance(l, BoolLit):
            ans = r if l.value else BoolLit(True)
        elif isinstance(r, BoolLit):
            ans = r if r.value else stdNot(l)
        elif l == r:
            ans = BoolLit(True)

    elif name == 'xor' and len(args) == 2:
        l, r = args
        if isinstance(l, BoolLit) and isinstance(r, BoolLit):
            ans = BoolLit(l.value != r.value)
        elif isinstance(l, BoolLit):
            ans = stdNot(r) if l.value else r
        elif isinstance(r, BoolLit):
            ans = stdNot(l) if r.value else l
        elif l == r:
            ans = BoolLit(False)

    ####
    # Arithmetic operations
    # https://smtlib.cs.uiowa.edu/theories-Ints.shtml
    # https://smtlib.cs.uiowa.edu/theories-Reals.shtml

    elif name == '-' and len(args) == 1:
        operand, = args
        if isinstance(operand, IntLit):
            ans = IntLit(-operand.value)
        elif isinstance(operand, RealLit):
            ans = RealLit(-operand.value)
        elif isinstance(operand, FunAppTerm) and operand.funName == '-' and len(operand.args) == 1:
            ans, = operand.args

    elif name == '+' and len(args) == 2:
        l, r = args

        if isinstance(l, IntLit) and isinstance(r, IntLit):
            ans = IntLit(l.value + r.value)
        elif isinstance(l, IntLit) and l.value == 0:
            ans = r
        elif isinstance(r, IntLit) and r.value == 0:
            ans = l

        elif isinstance(l, RealLit) and isinstance(r, RealLit):
            ans = RealLit(l.value + r.value)
        elif isinstance(l, RealLit) and l.value == 0:
            ans = r
        elif isinstance(r, RealLit) and r.value == 0:
            ans = l

    elif name == '-' and len(args) == 2:
        l, r = args

        if isinstance(l, IntLit) and isinstance(r, IntLit):
            ans = IntLit(l.value - r.value)
        elif isinstance(l, IntLit) and l.value == 0:
            ans = stdNeg(r)
        elif isinstance(r, IntLit) and r.value == 0:
            ans = l

        elif isinstance(l, RealLit) and isinstance(r, RealLit):
            ans = RealLit(l.value - r.value)
        elif isinstance(l, RealLit) and l.value == 0:
            ans = stdNeg(r)
        elif isinstance(r, RealLit) and r.value == 0:
            ans = l

    elif name == '*' and len(args) == 2:
        l, r = args

        if isinstance(l, IntLit) and isinstance(r, IntLit):
            ans = IntLit(l.value * r.value)
        elif isinstance(l, IntLit) and l.value == 1:
            ans = r
        elif isinstance(r, IntLit) and r.value == 1:
            ans = l
        elif isinstance(l, IntLit) and l.value == 0:
            ans = l
        elif isinstance(r, IntLit) and r.value == 0:
            ans = r

        elif isinstance(l, RealLit) and isinstance(r, RealLit):
            ans = RealLit(l.value * r.value)
        elif isinstance(l, RealLit) and l.value == 1:
            ans = r
        elif isinstance(r, RealLit) and r.value == 1:
            ans = l
        elif isinstance(l, RealLit) and l.value == 0:
            ans = l
        elif isinstance(r, RealLit) and r.value == 0:
            ans = r

    # For the division operations, we can't simplify the x / x form unless we can show that x != 0
    # because division by 0 in SMT-LIB has funny semantics.

    elif name == 'div' and len(args) == 2:
        l, r = args
        if isinstance(l, IntLit) and isinstance(r, IntLit) and r.value != 0:
            ans = IntLit(intDiv(l.value, r.value))
        elif isinstance(r, IntLit) and r.value == 1:
            ans = l

    elif name == '/' and len(args) == 2:
        l, r = args
        if isinstance(l, RealLit) and isinstance(r, RealLit) and r.value != 0.0:
            ans = RealLit(l.value / r.value)
        elif isinstance(r, RealLit) and r.value == 1.0:
            ans = l

    elif name == 'mod' and len(args) == 2:
        l, r = args
        if isinstance(l, IntLit) and isinstance(r, IntLit) and r.value != 0:
            ans = IntLit(intMod(l.value, r.value))
        elif isinstance(r, IntLit) and r.value == 1:
            ans = IntLit(0)

    elif name == 'abs' and len(args) == 1:
        operand, = args

        if isinstance(operand, IntLit):
            ans = IntLit(abs(operand.value))
        elif isinstance(operand, FunAppTerm) and operand.funName == '-' and len(operand.args) == 1:
            ans = stdAbs(operator.args)

        elif isinstance(operand, RealLit):
            ans = RealLit(abs(operand.value))
        elif isinstance(operand, FunAppTerm) and operand.funName == '-' and len(operand.args) == 1:
            ans = stdAbs(operator.args)

    ####
    # Numerical inequalities

    elif name == '>' and len(args) == 2:
        l, r = args

        if isinstance(l, IntLit) and isinstance(r, IntLit):
            ans = BoolLit(l.value > r.value)
        elif l == r:
            ans = BoolLit(False)
        elif isinstance(l, RealLit) and isinstance(r, RealLit):
            ans = BoolLit(l.value > r.value)

    elif name == '>=' and len(args) == 2:
        l, r = args

        if isinstance(l, IntLit) and isinstance(r, IntLit):
            ans = BoolLit(l.value >= r.value)
        elif l == r:
            ans = BoolLit(True)
        elif isinstance(l, RealLit) and isinstance(r, RealLit):
            ans = BoolLit(l.value >= r.value)

    elif name == '<' and len(args) == 2:
        l, r = args

        if isinstance(l, IntLit) and isinstance(r, IntLit):
            ans = BoolLit(l.value < r.value)
        elif l == r:
            ans = BoolLit(False)
        elif isinstance(l, RealLit) and isinstance(r, RealLit):
            ans = BoolLit(l.value < r.value)

    elif name == '<=' and len(args) == 2:
        l, r = args

        if isinstance(l, IntLit) and isinstance(r, IntLit):
            ans = BoolLit(l.value <= r.value)
        elif l == r:
            ans = BoolLit(True)
        elif isinstance(l, RealLit) and isinstance(r, RealLit):
            ans = BoolLit(l.value <= r.value)

    ####
    # String operations
    # https://smtlib.cs.uiowa.edu/theories-UnicodeStrings.shtml

    elif name == 'str.++' and len(args) == 2:
        l, r = args

        if isinstance(l, StringLit) and isinstance(r, StringLit):
            ans = StringLit(l.value + r.value)
        elif isinstance(l, StringLit) and l.value == '':
            ans = r
        elif isinstance(r, StringLit) and r.value == '':
            ans = l

    elif name == 'str.at' and len(args) == 2:
        l, r = args

        if isinstance(l, StringLit) and isinstance(r, IntLit):
            ans = StringLit(l.value[r.value]) if 0 <= r.value < len(l.value) else StringLit('')
        elif isinstance(l, StringLit) and l.value == '':
            ans = StringLit('')
        elif isinstance(r, IntLit) and r.value < 0:
            ans = StringLit('')

    elif name == 'str.substr' and len(args) == 3:
        s, i, n = args

        if isinstance(s, StringLit) and isinstance(i, IntLit) and isinstance(n, IntLit):
            if n.value <= 0: ans = StringLit('')
            elif 0 <= i.value < len(s.value): ans = StringLit(s.value[i.value:i.value + n.value])
            else: ans = StringLit('')
        elif isinstance(s, StringLit) and isinstance(i, IntLit) and len(s.value) <= i.value:
            ans = StringLit('')
        elif isinstance(i, IntLit) and i.value < 0:
            ans = StringLit('')
        elif isinstance(n, IntLit) and n.value < 0:
            ans = StringLit('')

    elif name == 'str.indexof' and len(args) == 3:
        s, t, i = args

        # From the SMT-LIB description:
        # 1. (str.indexof s t i), with 0 <= i <= |s| is the position of the first occurrence of t in s at or after
        #    position i, if any. Otherwise, it is -1.
        # 2. Note that the result is i whenever i is within the range [0, |s|] and t is empty.

        if isinstance(s, StringLit) and isinstance(t, StringLit) and isinstance(i, IntLit):
            if 0 <= i.value < len(s.value):
                ans = IntLit(s.value[i.value:].find(t.value))
            else:
                ans = IntLit(-1)
        elif isinstance(s, StringLit) and isinstance(i, IntLit):
            if i.value < 0 or len(s.value) <= i.value:
                ans = IntLit(-1)

    elif name == 'str.replace' and len(args) == 3:
        s, t1, t2 = args

        # 1. (str.replace s t t') is the string obtained by replacing the first occurrence of t in s, if any, by t'.
        # 2. Note that if t is empty, the result is to prepend t' to s;
        #    also, if t does not occur in s then the result is s.

        if isinstance(s, StringLit) and isinstance(t1, StringLit) and isinstance(t2, StringLit):
            ans = StringLit(s.value.replace(t1.value, t2.value, 1))
        elif isinstance(t1, StringLit) and t1.value == '':
            if isinstance(t2, StringLit) and t2.value == '':
                ans = s
            else:
                ans = stdConcat(t2, s)

    elif name == 'str.from_int' and len(args) == 1:
        n, = args

        # (str.from_int n) with n non-negative is the corresponding string in decimal notation, with no leading zeros.
        # If n < 0, it is the empty string.

        if isinstance(n, IntLit):
            ans = StringLit(str(n) if n.value >= 0 else '')

    elif name == 'str.len' and len(args) == 1:
        s, = args
        if isinstance(s, StringLit):
            ans = IntLit(len(s.value))

    elif name == 'str.to_int' and len(args) == 1:
        s, = args

        # 1. (str.to_int s) with s consisting of digits (in the sense of str.is_digit) evaluates to the positive integer
        #    denoted by s when seen as a number in  base 10 (possibly with leading zeros).
        # 2. It evaluates to -1 if s is empty or contains non-digits.

        if isinstance(s, StringLit):
            if len(s.value) > 0:
                try:
                    ans = IntLit(int(s.value))
                except:
                    ans = IntLit(-1)
            else:
                ans = IntLit(-1)

    elif name == 'str.contains' and len(args) == 2:
        s, t = args

        if isinstance(s, StringLit) and isinstance(t, StringLit):
            ans = BoolLit(t.value in s.value)
        elif isinstance(t, StringLit) and t.value == '':
            ans = BoolLit(True)

    elif name == 'str.prefixof' and len(args) == 2:
        s, t = args

        if isinstance(s, StringLit) and isinstance(t, StringLit):
            ans = BoolLit(t.value.startswith(s.value))
        elif isinstance(s, StringLit) and s.value == '':
            ans = BoolLit(True)

    elif name == 'str.suffixof' and len(args) == 2:
        s, t = args

        if isinstance(s, StringLit) and isinstance(t, StringLit):
            ans = BoolLit(t.value.endswith(s.value))
        elif isinstance(s, StringLit) and s.value == '':
            ans = BoolLit(True)

    elif name == 'str.<' and len(args) == 2:
        s, t = args

        if isinstance(s, StringLit) and isinstance(t, StringLit):
            ans = BoolLit(s.value < t.value)
        elif isinstance(s, StringLit) and s.value == '':
            ans = BoolLit(True)

    elif name == 'str.<=' and len(args) == 2:
        s, t = args

        if isinstance(s, StringLit) and isinstance(t, StringLit):
            ans = BoolLit(s.value <= t.value)
        elif isinstance(s, StringLit) and s.value == '':
            ans = BoolLit(True)

    ####
    # Bit-vector operations
    # https://smtlib.cs.uiowa.edu/theories-FixedSizeBitVectors.shtml

    elif name == 'bvnot' and len(args) == 1:
        operand, = args

        if isinstance(operand, BVLit):
            ans = BVLit(value=(1 << operand.length) - operand.value - 1, length=operand.length)
        elif isinstance(operand, FunAppTerm) and operand.funName == 'bvnot' and len(operand.args) == 1:
            ans, = operand.args

    elif name == 'bvand' and len(args) == 2:
        s, t = args

        if isinstance(s, BVLit) and isinstance(t, BVLit):
            assert s.length == t.length
            ans = BVLit(value=s.value & t.value, length=s.length)
        elif isinstance(s, BVLit) and s.value == 0:
            ans = s
        elif isinstance(t, BVLit) and t.value == 0:
            ans = t
        elif isinstance(s, BVLit) and s.value == (1 << s.length) - 1:
            ans = t
        elif isinstance(t, BVLit) and t.value == (1 << t.length) - 1:
            ans = s

    elif name == 'bvor' and len(args) == 2:
        s, t = args

        if isinstance(s, BVLit) and isinstance(t, BVLit):
            assert s.length == t.length
            ans = BVLit(value=s.value | t.value, length=s.length)
        elif isinstance(s, BVLit) and s.value == 0:
            ans = t
        elif isinstance(t, BVLit) and t.value == 0:
            ans = s
        elif isinstance(s, BVLit) and s.value == (1 << s.length) - 1:
            ans = s
        elif isinstance(t, BVLit) and t.value == (1 << t.length) - 1:
            ans = t

    elif name == 'bvxor' and len(args) == 2:
        s, t = args

        if isinstance(s, BVLit) and isinstance(t, BVLit):
            assert s.length == t.length
            ans = BVLit(value=s.value ^ t.value, length=s.length)
        elif isinstance(s, BVLit) and s.value == 0:
            ans = t
        elif isinstance(t, BVLit) and t.value == 0:
            ans = s
        elif isinstance(s, BVLit) and s.value == (1 << s.length) - 1:
            ans = stdBVNot(t)
        elif isinstance(t, BVLit) and t.value == (1 << t.length) - 1:
            ans = stdBVNot(s)

    elif name == 'bvneg' and len(args) == 1:
        operand, = args

        if isinstance(operand, BVLit):
            ans = (1 << operand.length) - operand.value
            ans = ans % (1 << operand.length)
            ans = BVLit(value=ans, length=operand.length)
        elif isinstance(operand, FunAppTerm) and operand.funName == 'bvnot' and len(operand.args) == 1:
            ans, = operand.args

    elif name == 'bvadd' and len(args) == 2:
        s, t = args

        if isinstance(s, BVLit) and isinstance(t, BVLit):
            assert s.length == t.length
            ans = s.value + t.value
            ans = ans % (1 << s.length)
            ans = BVLit(value=ans, length=s.length)
        elif isinstance(s, BVLit) and s.value == 0:
            ans = t
        elif isinstance(t, BVLit) and t.value == 0:
            ans = s

    elif name == 'bvsub' and len(args) == 2:
        s, t = args

        if isinstance(s, BVLit) and isinstance(t, BVLit):
            assert s.length == t.length
            ans = s.value - t.value
            if ans < 0: ans = ans + (1 << s.length)
            assert 0 <= ans < (1 << s.length)
            ans = BVLit(value=ans, length=s.length)
        elif isinstance(s, BVLit) and s.value == 0:
            ans = stdBVNeg(t)
        elif isinstance(t, BVLit) and t.value == 0:
            ans = s

    elif name == 'bvmul' and len(args) == 2:
        s, t = args

        if isinstance(s, BVLit) and isinstance(t, BVLit):
            assert s.length == t.length
            ans = (s.value * t.value) % (1 << s.length)
            ans = BVLit(value=ans, length=s.length)
        elif isinstance(s, BVLit) and s.value == 0:
            ans = s
        elif isinstance(t, BVLit) and t.value == 0:
            ans = t
        elif isinstance(s, BVLit) and s.value == 1:
            ans = t
        elif isinstance(t, BVLit) and t.value == 1:
            ans = s

    elif name == 'bvudiv' and len(args) == 2:
        s, t = args

        if isinstance(s, BVLit) and isinstance(t, BVLit):
            assert s.length == t.length
            ans = intDiv(s.value, t.value) if t.value != 0 else 1
            ans = BVLit(value=ans, length=s.length)
        elif isinstance(t, BVLit) and t.value == 0:
            ans = BVLit(value=1, length=t.length)
        elif isinstance(t, BVLit) and t.value == 1:
            ans = s

    elif name == 'bvurem' and len(args) == 2:
        s, t = args

        if isinstance(s, BVLit) and isinstance(t, BVLit):
            assert s.length == t.length
            ans = intMod(s.value, t.value) if t.value != 0 else s.value
            ans = BVLit(value=ans, length=s.length)
        elif isinstance(t, BVLit) and t.value == 0:
            ans = s
        elif isinstance(t, BVLit) and t.value == 1:
            ans = BVLit(value=0, length=t.length)

    elif name == 'bvshl' and len(args) == 2:
        s, t = args

        if isinstance(s, BVLit) and isinstance(t, BVLit):
            assert s.length == t.length
            ans = s.value << t.value
            ans = ans % (1 << s.length)
            ans = BVLit(value=ans, length=s.length)
        elif isinstance(s, BVLit) and s.value == 0:
            ans = s
        elif isinstance(t, BVLit) and t.value == 0:
            ans = s

    elif name == 'bvlshr' and len(args) == 2:
        s, t = args

        if isinstance(s, BVLit) and isinstance(t, BVLit):
            assert s.length == t.length
            ans = s.value >> t.value
            ans = BVLit(value=ans, length=s.length)
        elif isinstance(s, BVLit) and s.value == 0:
            ans = s
        elif isinstance(t, BVLit) and t.value == 0:
            ans = s

    elif name == 'bvashr' and len(args) == 2:
        s, t = args

        if isinstance(s, BVLit) and isinstance(t, BVLit):
            assert s.length == t.length
            ans = s.value >> t.value
            if s.value >= (1 << (s.length - 1)):
                if t.value < s.length:
                    remBits = s.length - t.value
                    mask = ((1 << s.length) - 1) - ((1 << remBits) - 1)
                    ans = ans | mask
                else:
                    ans = (1 << s.length) - 1
            ans = BVLit(value=ans, length=s.length)
        elif isinstance(s, BVLit) and s.value == 0:
            ans = s
        elif isinstance(t, BVLit) and t.value == 0:
            ans = s

    return ans

####

def intDiv(numerator, denominator):
    assert denominator != 0
    if denominator > 0: return math.floor(numerator / denominator)
    else: return math.ceil(numerator / denominator)

def intMod(numerator, denominator):
    assert denominator != 0
    return numerator - denominator * intDiv(numerator, denominator)
