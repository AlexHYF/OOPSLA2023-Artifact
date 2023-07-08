(set-logic CHC_LIA)

(synth-fun invariant ((x_0 Int) (x_1 Int) (x_2 Int) (x_3 Int) (x_4 Int) (x_5 Int) (x_6 Int) (x_7 Int) (x_8 Int) (x_9 Bool) (x_10 Int) (x_11 Int) (x_12 Bool) (x_13 Int) (x_14 Int) (x_15 Bool) (x_16 Int) (x_17 Int)) Bool)

(constraint (forall ((state.pc!0 Int) (state.pc!1 Int) (state.pending Int) (state.did_not_pay Int) (state.paid_tax Int) (state.posted Int) (state.K Int) (state.ht!0!assimilated Bool) (state.ht!0!num_entries Int) (state.ht!0!num_to_migrate Int) (state.ht!1!assimilated Bool) (state.ht!1!num_entries Int) (state.ht!1!num_to_migrate Int) (state.ht!2!assimilated Bool) (state.ht!2!num_entries Int) (state.ht!2!num_to_migrate Int) (state.old Int) (state.new Int)) (=> (and (= state.pc!0 0) (= state.pc!1 0) (= state.pending 0) (= state.did_not_pay 0) (= state.paid_tax 0) (= state.posted 0) (= state.K 32) (= state.ht!0!assimilated false) (= state.ht!0!num_entries 0) (= state.ht!0!num_to_migrate 0) (= state.ht!1!assimilated false) (= state.ht!1!num_entries 0) (= state.ht!1!num_to_migrate 0) (= state.ht!2!assimilated false) (= state.ht!2!num_entries 0) (= state.ht!2!num_to_migrate 0) (= state.old 1) (= state.new 1) (or (= state.pc!0 0) (= state.pc!0 1) (= state.pc!0 2) (= state.pc!0 3)) (or (= state.pc!1 0) (= state.pc!1 1) (= state.pc!1 2) (= state.pc!1 3)) (or (= state.old 1) (= state.old 2) (= state.old 3)) (or (= state.new 1) (= state.new 2) (= state.new 3))) (invariant state.pc!0 state.pc!1 state.K state.old state.new state.pending state.did_not_pay state.paid_tax state.posted state.ht!0!assimilated state.ht!0!num_entries state.ht!0!num_to_migrate state.ht!1!assimilated state.ht!1!num_entries state.ht!1!num_to_migrate state.ht!2!assimilated state.ht!2!num_entries state.ht!2!num_to_migrate))))
(constraint (forall ((state.pc!0 Int) (state.pc!1 Int) (state.K Int) (state.old Int) (state.new Int) (state.pending Int) (state.did_not_pay Int) (state.paid_tax Int) (state.posted Int) (state.ht!0!assimilated Bool) (state.ht!0!num_entries Int) (state.ht!0!num_to_migrate Int) (state.ht!1!assimilated Bool) (state.ht!1!num_entries Int) (state.ht!1!num_to_migrate Int) (state.ht!2!assimilated Bool) (state.ht!2!num_entries Int) (state.ht!2!num_to_migrate Int) (next.ht!0!assimilated Bool) (next.ht!0!num_entries Int) (next.ht!0!num_to_migrate Int) (next.ht!1!assimilated Bool) (next.ht!1!num_entries Int) (next.ht!1!num_to_migrate Int) (next.ht!2!assimilated Bool) (next.ht!2!num_entries Int) (next.ht!2!num_to_migrate Int) (next.pending Int) (next.paid_tax Int) (next.pc!0 Int) (next.K Int) (next.did_not_pay Int) (next.new Int) (next.old Int) (next.posted Int) (next.pc!1 Int)) (let ((a!1 (ite (= state.old 3) state.ht!2!assimilated (ite (= state.old 2) state.ht!1!assimilated state.ht!0!assimilated))) (a!2 (ite (= state.old 3) state.ht!2!num_to_migrate (ite (= state.old 2) state.ht!1!num_to_migrate state.ht!0!num_to_migrate))) (a!3 (ite (= state.new 3) state.ht!2!assimilated (ite (= state.new 2) state.ht!1!assimilated state.ht!0!assimilated))) (a!6 (ite (= state.new 3) state.ht!2!num_entries (ite (= state.new 2) state.ht!1!num_entries state.ht!0!num_entries))) (a!12 (ite (= state.new 3) state.ht!2!num_to_migrate (ite (= state.new 2) state.ht!1!num_to_migrate state.ht!0!num_to_migrate))) (a!24 (and (= next.ht!0!assimilated state.ht!0!assimilated) (= next.ht!0!num_entries state.ht!0!num_entries) (= next.ht!0!num_to_migrate state.ht!0!num_to_migrate) (= next.ht!1!assimilated state.ht!1!assimilated) (= next.ht!1!num_entries state.ht!1!num_entries) (= next.ht!1!num_to_migrate state.ht!1!num_to_migrate) (= next.ht!2!assimilated state.ht!2!assimilated) (= next.ht!2!num_entries state.ht!2!num_entries) (= next.ht!2!num_to_migrate state.ht!2!num_to_migrate))) (a!27 (ite (= (+ state.new 1) 3) state.ht!2!assimilated (ite (= (+ state.new 1) 2) state.ht!1!assimilated state.ht!0!assimilated))) (a!37 (ite (= (+ state.new 1) 2) (ite (= (+ state.new 1) 2) 0 state.ht!1!num_entries) (ite (= (+ state.new 1) 1) 0 state.ht!0!num_entries))) (a!46 (ite (= (+ state.new 1) 3) state.ht!2!num_to_migrate (ite (= (+ state.new 1) 2) state.ht!1!num_to_migrate state.ht!0!num_to_migrate)))) (let ((a!4 (ite (= state.old 3) (ite (= state.new 3) a!3 state.ht!2!assimilated) (ite (= state.old 2) (ite (= state.new 2) a!3 state.ht!1!assimilated) (ite (= state.new 1) a!3 state.ht!0!assimilated)))) (a!7 (ite (= state.new 3) (+ a!6 (ite (< 8 a!2) 8 a!2)) state.ht!2!num_entries)) (a!8 (ite (= state.new 2) (+ a!6 (ite (< 8 a!2) 8 a!2)) state.ht!1!num_entries)) (a!9 (ite (= state.new 1) (+ a!6 (ite (< 8 a!2) 8 a!2)) state.ht!0!num_entries)) (a!13 (ite (= state.old 1) (- a!2 (ite (< 8 a!2) 8 a!2)) (ite (= state.new 1) a!12 state.ht!0!num_to_migrate))) (a!17 (ite (= state.old 2) (- a!2 (ite (< 8 a!2) 8 a!2)) (ite (= state.new 2) a!12 state.ht!1!num_to_migrate))) (a!21 (ite (= state.old 3) (- a!2 (ite (< 8 a!2) 8 a!2)) (ite (= state.new 3) a!12 state.ht!2!num_to_migrate))) (a!25 (and (= next.ht!0!assimilated (ite (= state.new 1) a!3 state.ht!0!assimilated)) (= next.ht!0!num_entries (ite (= state.new 1) (+ a!6 1) state.ht!0!num_entries)) (= next.ht!0!num_to_migrate (ite (= state.new 1) a!12 state.ht!0!num_to_migrate)) (= next.ht!1!assimilated (ite (= state.new 2) a!3 state.ht!1!assimilated)) (= next.ht!1!num_entries (ite (= state.new 2) (+ a!6 1) state.ht!1!num_entries)) (= next.ht!1!num_to_migrate (ite (= state.new 2) a!12 state.ht!1!num_to_migrate)) (= next.ht!2!assimilated (ite (= state.new 3) a!3 state.ht!2!assimilated)) (= next.ht!2!num_entries (ite (= state.new 3) (+ a!6 1) state.ht!2!num_entries)) (= next.ht!2!num_to_migrate (ite (= state.new 3) a!12 state.ht!2!num_to_migrate)))) (a!26 (not (<= a!6 (* state.K (div 3 5))))) (a!28 (ite (= (+ state.new 1) 2) (ite (= (+ state.new 1) 2) a!27 state.ht!1!assimilated) (ite (= (+ state.new 1) 1) a!27 state.ht!0!assimilated))) (a!38 (ite (= (+ state.new 1) 3) (ite (= (+ state.new 1) 3) 0 state.ht!2!num_entries) a!37)) (a!47 (ite (= (+ state.new 1) 3) 0 (ite (= (+ state.new 1) 3) a!46 state.ht!2!num_to_migrate))) (a!48 (ite (= (+ state.new 1) 2) 0 (ite (= (+ state.new 1) 2) a!46 state.ht!1!num_to_migrate))) (a!49 (ite (= (+ state.new 1) 1) 0 (ite (= (+ state.new 1) 1) a!46 state.ht!0!num_to_migrate))) (a!57 (and (= state.pc!0 2) (<= a!6 (* state.K (div 3 5))) (= next.pc!0 3) (= next.K state.K) (= next.did_not_pay state.did_not_pay) a!24 (= next.new state.new) (= next.old state.old) (= next.paid_tax state.paid_tax) (= next.pending state.pending) (= next.posted state.posted))) (a!59 (and (= state.pc!1 2) (<= a!6 (* state.K (div 3 5))) (= next.pc!1 3) (= next.K state.K) (= next.did_not_pay state.did_not_pay) a!24 (= next.new state.new) (= next.old state.old) (= next.paid_tax state.paid_tax) (= next.pending state.pending) (= next.posted state.posted)))) (let ((a!5 (ite (= state.old 1) (<= a!2 8) (ite (= state.old 1) a!4 (ite (= state.new 1) a!3 state.ht!0!assimilated)))) (a!10 (ite (= state.old 3) a!7 (ite (= state.old 2) a!8 a!9))) (a!14 (ite (= state.old 1) (- a!2 (ite (< 8 a!2) 8 a!2)) a!13)) (a!15 (ite (= state.old 2) (<= a!2 8) (ite (= state.old 2) a!4 (ite (= state.new 2) a!3 state.ht!1!assimilated)))) (a!18 (ite (= state.old 2) (- a!2 (ite (< 8 a!2) 8 a!2)) a!17)) (a!19 (ite (= state.old 3) (<= a!2 8) (ite (= state.old 3) a!4 (ite (= state.new 3) a!3 state.ht!2!assimilated)))) (a!22 (ite (= state.old 3) (- a!2 (ite (< 8 a!2) 8 a!2)) a!21)) (a!29 (ite (= (+ state.new 1) 3) (ite (= (+ state.new 1) 3) a!27 state.ht!2!assimilated) a!28)) (a!39 (ite (= (+ state.new 1) 3) a!38 (ite (= (+ state.new 1) 3) 0 state.ht!2!num_entries))) (a!40 (ite (= (+ state.new 1) 2) a!38 (ite (= (+ state.new 1) 2) 0 state.ht!1!num_entries))) (a!41 (ite (= (+ state.new 1) 1) a!38 (ite (= (+ state.new 1) 1) 0 state.ht!0!num_entries))) (a!50 (ite (= (+ state.new 1) 3) a!47 (ite (= (+ state.new 1) 2) a!48 a!49)))) (let ((a!11 (= next.ht!0!num_entries (ite (= state.old 1) a!10 (ite (= state.old 1) a!10 a!9)))) (a!16 (= next.ht!1!num_entries (ite (= state.old 2) a!10 (ite (= state.old 2) a!10 a!8)))) (a!20 (= next.ht!2!num_entries (ite (= state.old 3) a!10 (ite (= state.old 3) a!10 a!7)))) (a!30 (ite (= (+ state.new 1) 3) a!29 (ite (= (+ state.new 1) 3) a!27 state.ht!2!assimilated))) (a!32 (ite (= (+ state.new 1) 2) a!29 (ite (= (+ state.new 1) 2) a!27 state.ht!1!assimilated))) (a!34 (ite (= (+ state.new 1) 1) a!29 (ite (= (+ state.new 1) 1) a!27 state.ht!0!assimilated))) (a!42 (ite (= (+ state.new 1) 3) a!39 (ite (= (+ state.new 1) 2) a!40 a!41))) (a!51 (ite (= state.new 1) a!6 (ite (= (+ state.new 1) 1) a!50 a!49))) (a!53 (ite (= state.new 2) a!6 (ite (= (+ state.new 1) 2) a!50 a!48))) (a!55 (ite (= state.new 3) a!6 (ite (= (+ state.new 1) 3) a!50 a!47)))) (let ((a!23 (and (= next.ht!0!assimilated a!5) a!11 (= next.ht!0!num_to_migrate a!14) (= next.ht!1!assimilated a!15) a!16 (= next.ht!1!num_to_migrate a!18) (= next.ht!2!assimilated a!19) a!20 (= next.ht!2!num_to_migrate a!22))) (a!31 (and (not (= (+ state.new 1) 3)) a!30)) (a!33 (and (not (= (+ state.new 1) 2)) a!32)) (a!35 (and (not (= (+ state.new 1) 1)) a!34)) (a!43 (ite (= state.new 2) (ite (= (+ state.new 1) 2) a!42 a!40) (ite (= (+ state.new 1) 1) a!42 a!41)))) (let ((a!36 (ite (= state.new 3) a!31 (ite (= state.new 2) a!33 a!35))) (a!44 (ite (= state.new 3) (ite (= (+ state.new 1) 3) a!42 a!39) a!43))) (let ((a!45 (ite (= state.new 1) a!44 (ite (= (+ state.new 1) 1) a!42 a!41))) (a!52 (ite (= state.new 2) a!44 (ite (= (+ state.new 1) 2) a!42 a!40))) (a!54 (ite (= state.new 3) a!44 (ite (= (+ state.new 1) 3) a!42 a!39)))) (let ((a!56 (and (= next.ht!0!assimilated (ite (= state.new 1) a!36 a!35)) (= next.ht!0!num_entries a!45) (= next.ht!0!num_to_migrate a!51) (= next.ht!1!assimilated (ite (= state.new 2) a!36 a!33)) (= next.ht!1!num_entries a!52) (= next.ht!1!num_to_migrate a!53) (= next.ht!2!assimilated (ite (= state.new 3) a!36 a!31)) (= next.ht!2!num_entries a!54) (= next.ht!2!num_to_migrate a!55)))) (let ((a!58 (or (and (= state.pc!0 0) (not (= state.old state.new)) (not a!1) a!23 (= next.pending (+ state.pending 1)) (= next.paid_tax (+ state.paid_tax 1)) (= next.pc!0 1) (= next.K state.K) (= next.did_not_pay state.did_not_pay) (= next.new state.new) (= next.old state.old) (= next.posted state.posted)) (and (= state.pc!0 0) (or (= state.old state.new) a!1) (= next.pc!0 1) (= next.pending (+ state.pending 1)) (= next.K state.K) (= next.did_not_pay state.did_not_pay) a!24 (= next.new state.new) (= next.old state.old) (= next.paid_tax state.paid_tax) (= next.posted state.posted)) (and (= state.pc!0 1) (= next.pending (- state.pending 1)) (= next.posted (+ state.posted 1)) (= next.pc!0 2) (= next.K state.K) (= next.did_not_pay state.did_not_pay) a!25 (= next.new state.new) (= next.old state.old) (= next.paid_tax state.paid_tax)) (and (= state.pc!0 2) a!26 (< state.new 3) (= next.K (* state.K 2)) (= next.old state.new) (= next.new (+ state.new 1)) a!56 (= next.did_not_pay state.pending) (= next.paid_tax 0) (= next.posted 0) (= next.pc!0 3) (= next.pending state.pending)) a!57 (and (= state.pc!0 2) a!26 (not (< state.new 3)) (= next.pc!0 4) (= next.K state.K) (= next.did_not_pay state.did_not_pay) a!24 (= next.new state.new) (= next.old state.old) (= next.paid_tax state.paid_tax) (= next.pending state.pending) (= next.posted state.posted)) (and (= state.pc!0 3) (= next.pc!0 0) (= next.K state.K) (= next.did_not_pay state.did_not_pay) a!24 (= next.new state.new) (= next.old state.old) (= next.paid_tax state.paid_tax) (= next.pending state.pending) (= next.posted state.posted)) (and (= state.pc!0 4) (= next.pc!0 4) (= next.K state.K) (= next.did_not_pay state.did_not_pay) a!24 (= next.new state.new) (= next.old state.old) (= next.paid_tax state.paid_tax) (= next.pending state.pending) (= next.posted state.posted)))) (a!60 (or (and (= state.pc!1 0) (not (= state.old state.new)) (not a!1) a!23 (= next.pending (+ state.pending 1)) (= next.paid_tax (+ state.paid_tax 1)) (= next.pc!1 1) (= next.K state.K) (= next.did_not_pay state.did_not_pay) (= next.new state.new) (= next.old state.old) (= next.posted state.posted)) (and (= state.pc!1 0) (or (= state.old state.new) a!1) (= next.pc!1 1) (= next.pending (+ state.pending 1)) (= next.K state.K) (= next.did_not_pay state.did_not_pay) a!24 (= next.new state.new) (= next.old state.old) (= next.paid_tax state.paid_tax) (= next.posted state.posted)) (and (= state.pc!1 1) (= next.pending (- state.pending 1)) (= next.posted (+ state.posted 1)) (= next.pc!1 2) (= next.K state.K) (= next.did_not_pay state.did_not_pay) a!25 (= next.new state.new) (= next.old state.old) (= next.paid_tax state.paid_tax)) (and (= state.pc!1 2) a!26 (< state.new 3) (= next.K (* state.K 2)) (= next.old state.new) (= next.new (+ state.new 1)) a!56 (= next.did_not_pay state.pending) (= next.paid_tax 0) (= next.posted 0) (= next.pc!1 3) (= next.pending state.pending)) a!59 (and (= state.pc!1 2) a!26 (not (< state.new 3)) (= next.pc!1 4) (= next.K state.K) (= next.did_not_pay state.did_not_pay) a!24 (= next.new state.new) (= next.old state.old) (= next.paid_tax state.paid_tax) (= next.pending state.pending) (= next.posted state.posted)) (and (= state.pc!1 3) (= next.pc!1 0) (= next.K state.K) (= next.did_not_pay state.did_not_pay) a!24 (= next.new state.new) (= next.old state.old) (= next.paid_tax state.paid_tax) (= next.pending state.pending) (= next.posted state.posted)) (and (= state.pc!1 4) (= next.pc!1 4) (= next.K state.K) (= next.did_not_pay state.did_not_pay) a!24 (= next.new state.new) (= next.old state.old) (= next.paid_tax state.paid_tax) (= next.pending state.pending) (= next.posted state.posted))))) (let ((a!61 (and (invariant state.pc!0 state.pc!1 state.K state.old state.new state.pending state.did_not_pay state.paid_tax state.posted state.ht!0!assimilated state.ht!0!num_entries state.ht!0!num_to_migrate state.ht!1!assimilated state.ht!1!num_entries state.ht!1!num_to_migrate state.ht!2!assimilated state.ht!2!num_entries state.ht!2!num_to_migrate) (or (and a!58 (= next.pc!1 state.pc!1)) (and a!60 (= next.pc!0 state.pc!0))) (or (= state.pc!0 0) (= state.pc!0 1) (= state.pc!0 2) (= state.pc!0 3)) (or (= state.pc!1 0) (= state.pc!1 1) (= state.pc!1 2) (= state.pc!1 3)) (or (= state.old 1) (= state.old 2) (= state.old 3)) (or (= state.new 1) (= state.new 2) (= state.new 3)) (or (= next.pc!0 0) (= next.pc!0 1) (= next.pc!0 2) (= next.pc!0 3)) (or (= next.pc!1 0) (= next.pc!1 1) (= next.pc!1 2) (= next.pc!1 3)) (or (= next.old 1) (= next.old 2) (= next.old 3)) (or (= next.new 1) (= next.new 2) (= next.new 3))))) (=> a!61 (invariant next.pc!0 next.pc!1 next.K next.old next.new next.pending next.did_not_pay next.paid_tax next.posted next.ht!0!assimilated next.ht!0!num_entries next.ht!0!num_to_migrate next.ht!1!assimilated next.ht!1!num_entries next.ht!1!num_to_migrate next.ht!2!assimilated next.ht!2!num_entries next.ht!2!num_to_migrate))))))))))))))
(constraint (forall ((state.pc!0 Int) (state.pc!1 Int) (state.K Int) (state.old Int) (state.new Int) (state.pending Int) (state.did_not_pay Int) (state.paid_tax Int) (state.posted Int) (state.ht!0!assimilated Bool) (state.ht!0!num_entries Int) (state.ht!0!num_to_migrate Int) (state.ht!1!assimilated Bool) (state.ht!1!num_entries Int) (state.ht!1!num_to_migrate Int) (state.ht!2!assimilated Bool) (state.ht!2!num_entries Int) (state.ht!2!num_to_migrate Int)) (let ((a!1 (<= (ite (= state.new 3) state.ht!2!num_entries (ite (= state.new 2) state.ht!1!num_entries state.ht!0!num_entries)) (* state.K (div 3 5))))) (let ((a!2 (not (or (not (= state.pc!0 3)) (not (= state.pc!1 3)) a!1)))) (=> (and (invariant state.pc!0 state.pc!1 state.K state.old state.new state.pending state.did_not_pay state.paid_tax state.posted state.ht!0!assimilated state.ht!0!num_entries state.ht!0!num_to_migrate state.ht!1!assimilated state.ht!1!num_entries state.ht!1!num_to_migrate state.ht!2!assimilated state.ht!2!num_entries state.ht!2!num_to_migrate) a!2) false)))))

(check-synth)

