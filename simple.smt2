(set-logic ALL_SUPPORTED)
(set-info :status unsat)

(declare-fun n () Int)
(declare-fun A () (Set Int))
(assert (= (card A) n))

(assert (> n 0))

(check-sat)
