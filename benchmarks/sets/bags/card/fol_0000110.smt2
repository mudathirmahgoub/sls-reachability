(set-logic ALL)


; forall a_gj:A. C(a_gj & ~f)

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

(declare-fun a_gj () (Bag Int))
; set semantics: a_gj has no repeated element
(assert (= a_gj (bag.setof a_gj)))
(assert (bag.subbag a_gj UNIVERALSET))
(assert (>= (bag.card a_gj) (- n t)))


(assert (not (>= (* 2 (bag.card (bag.inter_min a_gj (bag.difference_subtract UNIVERALSET f)))) (+ (- n t) 1))))

(check-sat)
