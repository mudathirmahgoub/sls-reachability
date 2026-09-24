(set-logic ALL)


; forall a_gn:A. forall a_gm:A. nonempty(a_gn & a_gm & ~f)

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

(declare-fun a_gn () (Bag Int))
; set semantics: a_gn has no repeated element
(assert (= a_gn (bag.setof a_gn)))
(assert (bag.subbag a_gn UNIVERALSET))
(assert (>= (bag.card a_gn) (- n t)))

(declare-fun a_gm () (Bag Int))
; set semantics: a_gm has no repeated element
(assert (= a_gm (bag.setof a_gm)))
(assert (bag.subbag a_gm UNIVERALSET))
(assert (>= (bag.card a_gm) (- n t)))


(assert (= (bag.card (bag.inter_min (bag.inter_min a_gn a_gm) (bag.difference_subtract UNIVERALSET f))) 0))

(check-sat)
