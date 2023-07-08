(set-logic QF_AUFLIA)
(set-info :source | This is based on an example in Section 6.2 of "A Decision
Procedure for an Extensional Theory of Arrays" by Stump, Barrett, Dill, and
Levitt. |)
(set-info :smt-lib-version 2.0)
(set-info :category "check")
(set-info :status unsat)
(set-info :notes |This benchmark is designed to require an array DP to propagate a properly entailed disjunction of equalities between shared terms.|)
(declare-fun a () (Array Int Int))
(declare-fun b () (Array Int Int))
(declare-fun v () Int)
(declare-fun w () Int)
(declare-fun x () Int)
(declare-fun y () Int)
(declare-fun g ((Array Int Int)) Int)
(declare-fun f (Int) Int)
(assert (and (= (store a x v) b) (= (store a y w) b) (not (= (f x) (f y))) (not (= (g a) (g b)))))
(check-sat)
(exit)
