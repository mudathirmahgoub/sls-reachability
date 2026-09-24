(set-logic ALL)


; forall b_bf:B. forall a_be:A. C(b_bf & a_be & f & ~f)

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

(declare-fun b_bf () (Bag Int))
; set semantics: b_bf has no repeated element
(assert (= b_bf (bag.setof b_bf)))
(assert (bag.subbag b_bf UNIVERALSET))
(assert (>= (* 2 (bag.card b_bf)) (+ (+ n (* 3 t)) 1)))

(declare-fun a_be () (Bag Int))
; set semantics: a_be has no repeated element
(assert (= a_be (bag.setof a_be)))
(assert (bag.subbag a_be UNIVERALSET))
(assert (>= (bag.card a_be) (- n t)))


(assert (not (>= (* 2 (bag.card (bag.inter_min (bag.inter_min (bag.inter_min b_bf a_be) f) (bag.difference_subtract UNIVERALSET f)))) (+ (- n t) 1))))

(check-sat)
