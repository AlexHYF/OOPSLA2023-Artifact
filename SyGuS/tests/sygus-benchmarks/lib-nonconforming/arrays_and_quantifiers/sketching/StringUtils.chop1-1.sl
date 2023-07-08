; org.apache.commons.lang3.StringUtils
; public static String chop(final String str)

; inputs
(declare-var |str.size| Int)
(declare-var |str| (Array Int Int))



(synth-fun |hole.size|
  (
    (|str.size| Int)
    (|str| (Array Int Int))
  )
  Int)


; helper
(define-fun ends_on_crlf
  (
    (|str| (Array Int Int))
    (|str.size| Int)
  )
  Bool
  (and
    (>= |str.size| 2)
    (= (select |str| (- |str.size| 2)) 13)
    (= (select |str| (- |str.size| 1)) 10)
  )
)

; postcondition when string ends on crlf

(constraint 
  (ite (ends_on_crlf |str| |str.size|)
  (= (|hole.size| |str.size| |str|) (- |str.size| 2))
  (ite (>= |str.size| 1)
  (= (|hole.size| |str.size| |str|)(- |str.size| 1) )
  (= (|hole.size| |str.size| |str|) |str.size|))))



(check-synth)
