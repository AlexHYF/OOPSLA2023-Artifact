import sexpdata as sp

#lam = sp.loads("(lambda (fold (fold $0 $0 (lambda (lambda (cdr ((lambda (lambda (fold $1 (cons $0 empty) (lambda (lambda (cons $1 $0)))))) $0 $1))))) $0 (lambda (lambda (cdr ((lambda (lambda (fold $1 (cons $0 empty) (lambda (lambda (cons $1 $0)))))) ((lambda (lambda (fold $1 (cons $0 empty) (lambda (lambda (cons $1 $0)))))) $0 $1) $1))))))")
#(lambda (v0) (car ((lambda (v1) (lambda (v2) (fold (cdr (v2 ((lambda (v3) (cdr (cdr v3))) v1))) v1 (lambda (v4) (lambda (v5) (cdr ((lambda (v6) (lambda (v7) (fold v6 (cons v7 empty) (lambda (v8) (lambda (v9) (cons v8 v9)))))) v5 (car v5)))))))) v0 (lambda (v10) v0))))

#(lambda (car ((lambda (lambda (fold (cdr ($0 ((lambda (cdr (cdr $0))) $1))) $1 (lambda (lambda (cdr ((lambda (lambda (fold $1 (cons $0 empty) (lambda (lambda (cons $1 $0)))))) $0 (car $0)))))))) $0 (lambda $1))))
class restorer:

    def __init__(self):
        self.ctn = 0

    def restore_lam(self, l, vstack=[]):
        ret = []
        is_lambda = False
        for tk in l:
            if isinstance(tk, sp.Symbol):
                val = tk._val
                assert(isinstance(val, str))
                if val == "lambda" or val == "lambdah":
                    ret.append(val)
                    var = "v" + str(self.ctn)
                    ret.append(var)
                    vstack.append(var)
                    is_lambda = True
                    self.ctn = self.ctn + 1
                elif val.startswith("$"):
                    offset = int(val[1:])
                    ret.append(vstack[-1 - offset])
                else:
                    ret.append(val)
            elif isinstance(tk, list):
                ret.append(self.restore_lam(tk, vstack))
            else:
                ret.append(tk)
        if is_lambda:
            vstack.pop()
        return ret
    def restore_lam_racket(self, l, vstack=[]):
        ret = []
        is_lambda = False
        for tk in l:
            if isinstance(tk, sp.Symbol):
                val = tk._val
                assert(isinstance(val, str))
                if val == "lambda" or val == "lambdah":
                    ret.append(val)
                    var = "v" + str(self.ctn)
                    ret.append([var])
                    vstack.append(var)
                    is_lambda = True
                    self.ctn = self.ctn + 1
                elif val.startswith("$"):
                    offset = int(val[1:])
                    ret.append(vstack[-1 - offset])
                else:
                    ret.append(val)
            elif isinstance(tk, list):
                ret.append(self.restore_lam_racket(tk, vstack))
            else:
                ret.append(tk)
        if is_lambda:
            vstack.pop()
        return ret




#re = restorer()
#print(sp.dumps(re.restore_lam_racket(lam), str_as = 'symbol').replace("fold", "fold-right"))
                
#(lambda (v0) (fold-right (fold-right v0 v0 (lambda (v1 v2) (cdr ((lambda (v3 v4) (fold-right v3 (cons v4 empty) (lambda (v5 v6) (cons v5 v6)))) v2 v1)))) v0 (lambda (v7) (lambda (v8) (cdr ((lambda (v9 v10) (fold-right v9 (cons v10 empty) (lambda (v11 v12) (cons v11 v12)))) ((lambda (v13 v14) (fold-right v13 (cons v14 empty) (lambda (v15 v16) (cons v15 v16)))) v8 v7) v7))))))