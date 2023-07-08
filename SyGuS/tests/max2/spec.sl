(set-logic LIA)

(synth-fun max_2 ((a Int) (b Int)) Int)

(declare-var x Int)
(declare-var y Int)
(constraint (>= (max_2 x y) x))
(constraint (>= (max_2 x y) y))
(constraint (or (= x (max_2 x y)) (= y (max_2 x y))))

(check-synth)
