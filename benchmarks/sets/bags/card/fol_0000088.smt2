(set-logic ALL)


; forall a_ds:A. forall a_dr:A. nonempty(a_ds & a_dr & ~f)

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

(declare-fun a_ds () (Bag Int))
; set semantics: a_ds has no repeated element
(assert (= a_ds (bag.setof a_ds)))
(assert (bag.subbag a_ds UNIVERALSET))
(assert (>= (bag.card a_ds) (- n t)))

(declare-fun a_dr () (Bag Int))
; set semantics: a_dr has no repeated element
(assert (= a_dr (bag.setof a_dr)))
(assert (bag.subbag a_dr UNIVERALSET))
(assert (>= (bag.card a_dr) (- n t)))


(assert (= (bag.card (bag.inter_min (bag.inter_min a_ds a_dr) (bag.difference_subtract UNIVERALSET f))) 0))

(check-sat)
