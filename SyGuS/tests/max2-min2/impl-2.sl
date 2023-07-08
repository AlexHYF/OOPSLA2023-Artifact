(
(define-fun max2 ((x Int) (y Int)) Int (ite (>= (+ x (* (- 1) y)) 0) x y))
(define-fun min2 ((x Int) (y Int)) Int (- (+ x y) (max2 x y)))
)
