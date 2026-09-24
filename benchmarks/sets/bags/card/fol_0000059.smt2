(set-logic ALL)


; forall a_bv:A. A(a_bv)

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

(declare-fun a_bv () (Bag Int))
; set semantics: a_bv has no repeated element
(assert (= a_bv (bag.setof a_bv)))
(assert (bag.subbag a_bv UNIVERALSET))
(assert (>= (bag.card a_bv) (- n t)))


(assert (not (>= (bag.card a_bv) (- n t))))

(check-sat)
