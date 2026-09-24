(set-logic ALL)


; forall a_v:A. forall a_u:A. C(a_v & a_u & ~f)

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

(declare-fun a_v () (Bag Int))
; set semantics: a_v has no repeated element
(assert (= a_v (bag.setof a_v)))
(assert (bag.subbag a_v UNIVERALSET))
(assert (>= (bag.card a_v) (- n t)))

(declare-fun a_u () (Bag Int))
; set semantics: a_u has no repeated element
(assert (= a_u (bag.setof a_u)))
(assert (bag.subbag a_u UNIVERALSET))
(assert (>= (bag.card a_u) (- n t)))


(assert (not (>= (* 2 (bag.card (bag.inter_min (bag.inter_min a_v a_u) (bag.difference_subtract UNIVERALSET f)))) (+ (- n t) 1))))

(check-sat)
