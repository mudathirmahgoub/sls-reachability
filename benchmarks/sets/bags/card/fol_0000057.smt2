(set-logic ALL)


; forall a_bu:A. A(a_bu & ~f)

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

(declare-fun a_bu () (Bag Int))
; set semantics: a_bu has no repeated element
(assert (= a_bu (bag.setof a_bu)))
(assert (bag.subbag a_bu UNIVERALSET))
(assert (>= (bag.card a_bu) (- n t)))


(assert (not (>= (bag.card (bag.inter_min a_bu (bag.difference_subtract UNIVERALSET f))) (- n t))))

(check-sat)
