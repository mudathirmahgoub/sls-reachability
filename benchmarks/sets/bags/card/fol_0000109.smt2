(set-logic ALL)


; forall a_gi:A. forall a_gh:A. C(a_gi & a_gh & ~f)

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

(declare-fun a_gi () (Bag Int))
; set semantics: a_gi has no repeated element
(assert (= a_gi (bag.setof a_gi)))
(assert (bag.subbag a_gi UNIVERALSET))
(assert (>= (bag.card a_gi) (- n t)))

(declare-fun a_gh () (Bag Int))
; set semantics: a_gh has no repeated element
(assert (= a_gh (bag.setof a_gh)))
(assert (bag.subbag a_gh UNIVERALSET))
(assert (>= (bag.card a_gh) (- n t)))


(assert (not (>= (* 2 (bag.card (bag.inter_min (bag.inter_min a_gi a_gh) (bag.difference_subtract UNIVERALSET f)))) (+ (- n t) 1))))

(check-sat)
