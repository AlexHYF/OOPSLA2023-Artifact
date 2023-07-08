(set-logic SAT)

(define-fun
  __node_init_top_0 (
    (top.usr.OK_a_0 Bool)
    (top.res.init_flag_a_0 Bool)
  ) Bool
  
  (and (= top.usr.OK_a_0 true) top.res.init_flag_a_0)
)

(define-fun
  __node_trans_top_0 (
    (top.usr.OK_a_1 Bool)
    (top.res.init_flag_a_1 Bool)
    (top.usr.OK_a_0 Bool)
    (top.res.init_flag_a_0 Bool)
  ) Bool
  
  (and (= top.usr.OK_a_1 true) (not top.res.init_flag_a_1))
)



(synth-inv str_invariant(
  (top.usr.OK Bool)
  (top.res.init_flag Bool)
))


(declare-primed-var top.usr.OK Bool)
(declare-primed-var top.res.init_flag Bool)

(define-fun
  init (
    (top.usr.OK Bool)
    (top.res.init_flag Bool)
  ) Bool
  
  (and (= top.usr.OK true) top.res.init_flag)
)

(define-fun
  trans (
    
    ;; Current state.
    (top.usr.OK Bool)
    (top.res.init_flag Bool)
    
    ;; Next state.
    (top.usr.OK! Bool)
    (top.res.init_flag! Bool)
  
  ) Bool
  
  (and (= top.usr.OK! true) (not top.res.init_flag!))
)

(define-fun
  prop (
    (top.usr.OK Bool)
    (top.res.init_flag Bool)
  ) Bool
  
  top.usr.OK
)

(inv-constraint str_invariant init trans prop)

(check-synth)
