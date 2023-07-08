(set-logic LIA)

(synth-fun max2 ((x Int) (y Int)) Int)
(synth-fun min2 ((x Int) (y Int)) Int)

(declare-var x Int)
(declare-var y Int)
(constraint (>= (max2 x y) x))
(constraint (>= (max2 x y) y))
(constraint (or (= x (max2 x y)) (= y (max2 x y))))
(constraint (= (+ x y) (+ (max2 x y) (min2 x y))))

(check-synth)
