(set-info :smt-lib-version 2.6)
(set-logic ALL)
(set-info :status sat)
(set-option :strings-exp true)
(set-option :re-elim false)
(declare-fun x () String)
(assert (let ((_let_0 (re.* re.allchar ))) (and (not (= (str.in_re x (re.++ _let_0 re.allchar  _let_0 (str.to_re (str.++ "B" (str.++ "A" (str.++ "C" "B")))) _let_0 re.allchar  _let_0)) (str.in_re x (re.++ _let_0 re.allchar  _let_0 (str.to_re (str.++ "A" (str.++ "B" (str.++ "C" "C")))) _let_0 re.allchar  _let_0)))) (not (= (str.in_re x (re.++ _let_0 re.allchar  _let_0 (str.to_re (str.++ "C" (str.++ "B" (str.++ "A" "B")))) _let_0 re.allchar  _let_0)) (str.in_re x (re.++ _let_0 re.allchar  _let_0 (str.to_re (str.++ "C" (str.++ "B" "A"))) _let_0 (str.to_re "B") _let_0)))))))
(check-sat)
