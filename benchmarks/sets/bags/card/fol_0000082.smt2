(set-logic ALL)


; forall b_di:B. forall b_dh:B. C(b_di & b_dh)

(declare-fun n () Int)
(declare-fun t () Int)

(declare-fun f () (Bag Int))
; set semantics: f has no repeated element
(assert (= f (bag.setof f)))
(declare-fun UNIVERALSET () (Bag Int))
; set semantics: UNIVERALSET has no repeated element
(assert (= UNIVERALSET (bag.setof UNIVERALSET)))
(assert (bag.subbag f UNIVERALSET))
(assert (= (bag.card UNIVERALSET) n))

(assert (> n 0))
(assert (> n (* 3 t)))
(assert (<= (bag.card f) t))

(declare-fun b_di () (Bag Int))
; set semantics: b_di has no repeated element
(assert (= b_di (bag.setof b_di)))
(assert (bag.subbag b_di UNIVERALSET))
(assert (>= (* 2 (bag.card b_di)) (+ (+ n (* 3 t)) 1)))

(declare-fun b_dh () (Bag Int))
; set semantics: b_dh has no repeated element
(assert (= b_dh (bag.setof b_dh)))
(assert (bag.subbag b_dh UNIVERALSET))
(assert (>= (* 2 (bag.card b_dh)) (+ (+ n (* 3 t)) 1)))


(assert (not (>= (* 2 (bag.card (bag.inter_min b_di b_dh))) (+ (- n t) 1))))

(check-sat)
