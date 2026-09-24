(set-logic ALL)


; forall a_ca:A. C(a_ca & ~f)

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

(declare-fun a_ca () (Bag Int))
; set semantics: a_ca has no repeated element
(assert (= a_ca (bag.setof a_ca)))
(assert (bag.subbag a_ca UNIVERALSET))
(assert (>= (bag.card a_ca) (- n t)))


(assert (not (>= (* 2 (bag.card (bag.inter_min a_ca (bag.difference_subtract UNIVERALSET f)))) (+ (- n t) 1))))

(check-sat)
