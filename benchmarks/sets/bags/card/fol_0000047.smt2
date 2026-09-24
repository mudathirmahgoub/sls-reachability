(set-logic ALL)


; forall b_x:B. forall a_w:A. C(b_x & a_w & ~f)

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

(declare-fun b_x () (Bag Int))
; set semantics: b_x has no repeated element
(assert (= b_x (bag.setof b_x)))
(assert (bag.subbag b_x UNIVERALSET))
(assert (>= (* 2 (bag.card b_x)) (+ (+ n (* 3 t)) 1)))

(declare-fun a_w () (Bag Int))
; set semantics: a_w has no repeated element
(assert (= a_w (bag.setof a_w)))
(assert (bag.subbag a_w UNIVERALSET))
(assert (>= (bag.card a_w) (- n t)))


(assert (not (>= (* 2 (bag.card (bag.inter_min (bag.inter_min b_x a_w) (bag.difference_subtract UNIVERALSET f)))) (+ (- n t) 1))))

(check-sat)
