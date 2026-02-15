(set-logic ALL_SUPPORTED)

(declare-fun f () (Set Int))
(declare-fun g () (Set Int))
(assert (distinct f g))
(assert (= emptyset f))
(check-sat)
