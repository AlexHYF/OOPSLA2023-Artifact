from contextlib import nullcontext
import math
from RestoreLambdas import restorer
import sexpdata as sp
import sys

def is_square(x):
    int(math.sqrt(x)) ** 2 == x

class evaluator:
    def __init__(self, exp):
       self.exp = exp
       self.binop = {
        '+' : lambda x, y : x + y,
        '-' : lambda x, y : x - y,
        '*' : lambda x, y : x * y,
        'cons' : lambda x, y : [x] + y,
        'eq?' : lambda x, y : x == y,
        'index' : lambda x, y : y[x],
        'gt?' : lambda x, y : x > y,
        'mod' : lambda x, y : x % y

       }
       self.unitop = {
        'car' : lambda x : x[0],
        'cdr' : lambda x : x[1:],
        'empty?' : lambda x : x == [],
        'is-prime' : lambda x : x in {
            2,
            3,
            5,
            7,
            11,
            13,
            17,
            19,
            23,
            29,
            31,
            37,
            41,
            43,
            47,
            53,
            59,
            61,
            67,
            71,
            73,
            79,
            83,
            89,
            97,
            101,
            103,
            107,
            109,
            113,
            127,
            131,
            137,
            139,
            149,
            151,
            157,
            163,
            167,
            173,
            179,
            181,
            191,
            193,
            197,
            199
        },
        'is-square' : lambda x : x >= 0 and int(math.sqrt(x)) ** 2 == x,
        #'is-square' : is_square,
        'range' : lambda x : list(range(x)),
        '-' : lambda x : -x,
        'length' : lambda x : len(x)
       }


    def _getConLocs(self, lam, stack=[],ret=[]):
        if isinstance(lam, list):
            if (lam[0] == "#"):
                stack.append(1)
                ret.append(stack.copy())
                self._getConLocs(lam[1], stack, ret)
                stack.pop()
            else:
                for i in range(len(lam)):
                    stack.append(i)
                    self._getConLocs(lam[i], stack, ret)
                    stack.pop()
        return ret
    def getConceptLocations(self):
        return self._getConLocs(self.exp) 

    def _is_constant(expr):
        if isinstance(expr, list):
            flag = True
            for l in expr:
                flag = flag and evaluator._is_constant(l)
            return flag
        elif isinstance(expr, int) or isinstance(expr, bool):
            return True
        else:
            return False



    def _partialEval(self, expr,inputs=[], binding_list={}, expanded_v={}):
        if evaluator._is_constant(expr):
            return expr
        elif isinstance(expr, str):
            if expr == "true":
                return True
            elif expr == "false":
                return False
            elif expr[0] == "v":
                if expr not in binding_list:
                    return expr
                expand = self._partialEval(binding_list[expr], inputs, binding_list, expanded_v)
                expanded_v[expr] = expand
                return expand
            elif expr == "empty":
                return []
            else:
                return expr
        elif isinstance(expr, list):
            if expr == []:
                return expr
            else:
                op = expr[0]
                if isinstance(op, str) and op[0] == "v":
                    if op not in binding_list:
                        return expr
                    expanded_v[op] = self._partialEval(binding_list[op], [],binding_list, expanded_v)
                    op = expanded_v[op]
                    #op = binding_list[op]
                if isinstance(op, str):
                    if op == "empty":
                        return []
                    elif op.startswith("lambda"):
                        flag = False
                        if len(inputs) != 0:
                            para = inputs.pop(0)
                            binding_list[expr[1]] = para
                            #para = self._partialEval(para, inputs, binding_list)
                        else:
                            flag = True
                        #    return expr
                        #binding_list[expr[1]] = para
                        ret = self._partialEval(expr[2], inputs, binding_list, expanded_v)
                        if not flag:
                            binding_list.pop(expr[1])
                        if op.startswith("lambdah"):
                            input_list = op.split("_")[1:]
                            return ["hole"] + [expanded_v[i] for i in input_list]
                        if flag:
                            return ["lambda", expr[1], ret]
                        return ret
                    elif op == "map":
                        if len(expr) == 3:
                            lst = self._partialEval(expr[2], inputs, binding_list, expanded_v)
                        else:
                            lst = inputs.pop(0)
                            lst = self._partialEval(lst, inputs, binding_list, expanded_v)
                        if evaluator._is_constant(lst):
                            ret = []
                            for l in lst:
                                inputs.insert(0, l)
                                ret.append(self._partialEval(expr[1], inputs, binding_list, expanded_v))
                            return ret
                        return ["map", self._partialEval(expr[1], [], binding_list, expanded_v), lst]
                    elif op == "fold":
                        lst = self._partialEval(expr[1])
                        init = self._partialEval(expr[2])
                        fun = self._partialEval(expr[3],[], binding_list,expanded_v)
                        if evaluator._is_constant(lst) and evaluator._is_constant(init):
                            ret = init
                            for l in lst[::-1]:
                                inputs.insert(0, l)
                                inputs.insert(1, ret)
                                ret = self._partialEval(fun, inputs, binding_list, expanded_v)
                            return ret
                        return ["fold", lst, init, fun]
                    elif op == "if":
                        cond = self._partialEval(expr[1], inputs, binding_list, expanded_v)
                        tb = self._partialEval(expr[2], inputs, binding_list, expanded_v)
                        fb = self._partialEval(expr[3], inputs, binding_list, expanded_v)
                        if evaluator._is_constant(cond):
                            if cond:
                                return tb
                            else:
                                return fb
                        return ["if", cond, tb, fb]
                    elif len(expr) == 3:
                        lop = self._partialEval(expr[1], inputs, binding_list, expanded_v)
                        rop = self._partialEval(expr[2], inputs, binding_list, expanded_v)
                        if evaluator._is_constant(lop) and evaluator._is_constant(rop):
                            if op in self.binop:
                                return self.binop[op](lop, rop)
                        return [op, lop, rop]
                    elif len(expr) == 2:
                        rop = self._partialEval(expr[1], inputs, binding_list, expanded_v)
                        if evaluator._is_constant(rop):
                            if op in self.unitop:
                                return self.unitop[op](rop)
                        return [op, rop]
                    else:
                        return expr
                elif isinstance(op, list):
                    if op[0].startswith("lambdah"):
                        numpara = len(op[0].split("_")) - 1
                        for para in reversed(expr[1:]):
                            inputs.insert(0, para)
                        ret = self._partialEval(op, inputs, binding_list, expanded_v)
                        if (numpara == len(expr) - 1):
                            return ret
                        else:
                            ret = [ret]
                            for v in expr[1+numpara:]:
                                ret.append(self._partialEval(v, inputs, binding_list, expanded_v))
                            return ret
                        
                    for para in reversed(expr[1:]):
                        inputs.insert(0, para)
                    return self._partialEval(op, inputs, binding_list, expanded_v)
                else:
                    return expr
        else:
            return expr

    def rewrite(self, expr):
        assert (expr[0] == "=")
        lop = expr[1]
        rop = expr[2]
        assert (evaluator._is_constant(rop))
        if (evaluator._is_constant(lop)):
            return [lop == rop]
        else:
            op = lop[0]
            if op == "+":
                lhs = lop[1]
                rhs = lop[2]
                if evaluator._is_constant(lhs):
                    return self.rewrite(['=', rhs, rop - lhs])
                elif evaluator._is_constant(rhs):
                    return self.rewrite(['=', lhs, rop - rhs])
                else:
                    return expr
            elif op == "-":
                lhs = lop[1]
                rhs = lop[2]
                if evaluator._is_constant(lhs):
                    return self.rewrite(['=', rhs, lhs - rop])
                elif evaluator._is_constant(rhs):
                    return self.rewrite(['=', lhs, rop + rhs])
                else:
                    return expr
            elif op == "*":
                lhs = lop[1]
                rhs = lop[2]
                if evaluator._is_constant(lhs):
                    return self.rewrite(['=', rhs, rop / lhs])
                elif evaluator._is_constant(rhs):
                    return self.rewrite(['=', lhs, rop / rhs])
                else:
                    return expr
            elif op == "cons":
                lhs = lop[1]
                rhs = lop[2]
                if evaluator._is_constant(lhs):
                    return self.rewrite(['=', rhs, rop[1:]])
                elif evaluator._is_constant(rhs):
                    return self.rewrite(['=', lhs, rop[0]])
                else:
                    return expr
            elif op == "map":
                fun = lop[1]
                lst = lop[2]
                if isinstance(lst, list) and isinstance(rop, list) and len(lst) == len(rop): # and evaluator._is_constant(lst):
                    ret = []
                    for i in range(len(lst)):
                        ret.append(self.rewrite((["=", [fun, lst[i]], rop[i]])))
                    return ret
                return expr
            else:
                return expr

 






                    
#(lambda (#(lambda (map (lambda (+ $0 $1)))) 1 $0))



#    def partialEval(self, input_example:list, output_example:list, loc_of_holes:list = []):
        #mark holes

        
#lam = sp.loads("(lambda (cdr (cdr $0)))")
import json

data = json.loads(open(sys.argv[1]).read())

#lam = sp.loads("(lambda (#(lambdah (cdr (#(lambda (lambda (map (lambda (index $0 $2)) (range $0)))) $0 (+ #(+ 1 (+ 1 1)) #(+ 1 (+ 1 1)))))) (#(lambda (lambda (fold (cdr ($0 (#(lambda (cdr (cdr $0))) $1))) $1 (lambda (lambda (cdr (#(lambda (lambda (fold $1 (cons $0 empty) (lambda (lambda (cons $1 $0)))))) $0 (car $0)))))))) $0 (lambda $1))))".replace("#", ""))
#re = restorer()
#lam = [re.restore_lam(lam), [1,2,3,4,5,6,7]] # [2, 3 , 5]
#lam = sp.loads("(lambda ((lambda (lambda ((lambda (lambda (fold $1 empty (lambda (lambda (fold ($2 $1 range) $0 (lambda (lambda (cons $3 $2))))))))) $1 (lambda (lambda (if ($2 $1) $3 empty)))))) $0 (lambda ((lambda (gt? $0 0)) (mod $0 (car $1))))))")
#print(lam)
#lam = sp.loads("(lambda v0 (fold v0 v0 (lambda v1 (lambda v2 (cdr ((lambda v3 (lambda v4 (fold v3 (cons v4 empty) (lambda v5 (lambda v6 (cons v5 v6)))))) v2 v1))))))")
#lam = [lam, [1,2,3]]
#print(sp.dumps(lam, str_as = 'symbol'))

#eva = evaluator(lam)


#exit(0)
eva = evaluator("")

def nth_repl(s, sub, repl, n):
    
    find = s.find(sub)
    # If find is not -1 we have found at least one match for the substring
    i = int(find != -1)
    # loop util we find the nth or we find no match
    while find != -1 and i != n:
        # find + 1 means we start searching from after the last match
        find = s.find(sub, find + 1)
        i += 1
    # If i is equal to n we found nth match so replace
    if i == n:

        return s[:find] + repl + s[find+len(sub):]
    return s


def bind_hole_with_var(expr):
    if isinstance(expr, list):
        if len(expr) > 0 and isinstance(expr[0], str) and expr[0] == "lambdah":
            varlist = [expr[1]]
            t = expr[2]
            while isinstance(t[0], str) and t[0]=="lambda":
                varlist.append(t[1])
                t = t[2]
            name = "lambdah"
            for v in varlist:
                name = name+ "_" + v
            ret = [name]
            for i in range(1, len(expr)):
                ret.append(bind_hole_with_var(expr[i]))
            return ret
        else:
            return [bind_hole_with_var(i) for i in expr]
    return expr
def cal_size(expr):
    if isinstance(expr, list):
        return sum([cal_size(i) for i in expr])
    else:
        return 1

def cal_triv_size(expr):
    if isinstance(expr, list):
        if len(expr) > 0 and isinstance(expr[0], str) and expr[0].startswith("lambdah"):
            return 1
        return sum([cal_triv_size(i) for i in expr])
    else:
        return 1


blacklist = open("impl_backlist.txt").readlines()

blacklist = [i.strip() for i in blacklist]

def calculate_size(expr):
    if isinstance(expr, list) and len(expr) > 0:
        ret = 0
        for i in expr:
            ret = ret + calculate_size(i)
        return ret
    else:
        return 1

def calculate_triv_size(expr):
    if isinstance(expr, list) and len(expr) > 0:
        if isinstance(expr[0], str) and expr[0].startswith("lambdah"):
            return 1
        ret = 0
        for i in expr:
            ret = ret + calculate_size(i)
        return ret
    else:
        return 1 
stats = [['spec_size', 'impl_size', 'triv_size', 'subspec_size']]
true_ctn = 0
for task in data:
    print("Processing task: " + task["name"])
    #if task["name"] != "reverse":
        #continue
    for impl in task["implementations"]:
        if impl in blacklist:
            continue
        print("Processing implementation: " + impl)

        #verifying if the implementation is indeed correct

        is_correct = True

        for test in task["examples"]:
            if test["i"] == []:
                continue
            re = restorer()
            lam = [re.restore_lam(sp.loads(impl.replace("#",""))), test['i']]
            result = eva._partialEval(lam)
            if result != test['o']:
                is_correct = False
                break

        if not is_correct:
            print("Wrong implementation!")
            continue


        num_lam = impl.count("#(lambda")
        impl_real_backup = impl
        impl_size = calculate_size(sp.loads(impl.replace('#', "")))

        for i in range(num_lam):
            subspec_set = set()
            spec_size = 0
            impl_real = nth_repl(impl_real_backup, "#(lambda", "(lambdah", i+1).replace("#", "")
            impl_real = sp.loads(impl_real)
            subspec_size = 0
            triv_size = 0

            print("Processing {}th concept".format(i))
        #passed = True
            for test in task["examples"]:
                if test["i"] == []:
                    continue
                spec_size = spec_size + calculate_size(["=", ["f", test['i']], test['o']])
                re = restorer()
                
                lam = [re.restore_lam(impl_real), test['i']]
                triv_size = triv_size + calculate_triv_size(["=", lam, test['o']])
                lam = bind_hole_with_var(lam)
                #print(sp.dumps(lam, str_as="symbol"))
                
                
                #try:
                result = eva._partialEval(lam)
                subspec = eva.rewrite(['=', result, test['o']])
                subspec_str = sp.dumps(subspec, str_as='symbol')
                if subspec_str in subspec_set:
                    continue
                subspec_set.add(subspec_str)
                print(subspec_str)
                #result = eva.rewrite(['=', result, test['o']])
                subspec_size = subspec_size + cal_size(['=', result, test['o']])
                #print(['=', result, test['o']])
                #print(subspec_size/triv_size)
                #if test['o'] != result:
                    #print(test['i'])
                    #print(test['o'])
                    #print(result)
                    #print('error')
                    #passed = False
                #except:
                    #pass
                #print(test['i'])
                #    print("crash")
                #print(test['i'])
            stats.append([spec_size,impl_size,triv_size,subspec_size])
        #if passed:
#print(true_ctn)
import csv
with open('DC.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')

    for l in stats:
        writer.writerow(l)


#((lambda (v0) (fold-right v0 v0 (lambda (v1 v2) (cdr ((lambda (v3 v4) (fold v3 (cons v4 empty) (lambda (v5 v6) (cons v5 v6)))) v2 v1))))) '(1 2 3))
#((lambda v0 (car ((lambda v1 (lambda v2 (fold (cdr (v2 ((lambda v3 (cdr (cdr v3))) v1))) v1 (lambda v4 (lambda v5 (cdr ((lambda v6 (lambda v7 (fold v6 (cons v7 empty) (lambda v8 (lambda v9 (cons v8 v9)))))) v5 (car v5)))))))) v0 (lambda v10 v0)))) (2 3 4 5))
