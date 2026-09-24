(set-logic ALL)


; forall a_eh:A. forall a_eg:A. forall a_ef:A. nonempty(a_eh & a_eg & a_ef & ~f)

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

(declare-fun a_eh () (Bag Int))
; set semantics: a_eh has no repeated element
(assert (= a_eh (bag.setof a_eh)))
(assert (bag.subbag a_eh UNIVERALSET))
(assert (>= (bag.card a_eh) (- n t)))

(declare-fun a_eg () (Bag Int))
; set semantics: a_eg has no repeated element
(assert (= a_eg (bag.setof a_eg)))
(assert (bag.subbag a_eg UNIVERALSET))
(assert (>= (bag.card a_eg) (- n t)))

(declare-fun a_ef () (Bag Int))
; set semantics: a_ef has no repeated element
(assert (= a_ef (bag.setof a_ef)))
(assert (bag.subbag a_ef UNIVERALSET))
(assert (>= (bag.card a_ef) (- n t)))


(assert (= (bag.card (bag.inter_min (bag.inter_min (bag.inter_min a_eh a_eg) a_ef) (bag.difference_subtract UNIVERALSET f))) 0))

(check-sat)
