(set-logic QF_ALL)
(set-info :status unsat)
(set-option :produce-models true)
(set-option :sets-ext true)
(declare-fun A () (Set (_ BitVec 2)))
(declare-fun B () (Set (_ BitVec 2)))
(declare-fun C () (Set (_ BitVec 2)))
(declare-fun D () (Set (_ BitVec 2)))

(declare-fun x () (_ BitVec 2))
(assert (not (member x A)))
(assert (not (member x B)))
(assert (not (member x C)))
(assert (not (member x D)))
(declare-fun y () (_ BitVec 2))
(assert (not (member y A)))
(assert (not (member y B)))
(assert (not (member y C)))
(assert (not (member y D)))
(declare-fun z () (_ BitVec 2))
(assert (not (member z A)))
(assert (not (member z B)))
(assert (not (member z C)))
(assert (not (member z D)))

(assert (distinct x y z))

(assert (= (card (union A (union B (union C D)))) 2))

(check-sat)
