; COMMAND-LINE: --no-check-models --produce-models --decision=internal
; EXPECT: sat
(set-logic ALL)
(set-info :status sat)
(assert (distinct (sin 1.0) 0.0))
(check-sat)
