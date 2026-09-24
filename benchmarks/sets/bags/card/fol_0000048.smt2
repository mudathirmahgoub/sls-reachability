(set-logic ALL)


; forall b_ba:B. forall b_z:B. forall a_y:A. C(b_ba & b_z & a_y & ~f)

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

(declare-fun b_ba () (Bag Int))
; set semantics: b_ba has no repeated element
(assert (= b_ba (bag.setof b_ba)))
(assert (bag.subbag b_ba UNIVERALSET))
(assert (>= (* 2 (bag.card b_ba)) (+ (+ n (* 3 t)) 1)))

(declare-fun b_z () (Bag Int))
; set semantics: b_z has no repeated element
(assert (= b_z (bag.setof b_z)))
(assert (bag.subbag b_z UNIVERALSET))
(assert (>= (* 2 (bag.card b_z)) (+ (+ n (* 3 t)) 1)))

(declare-fun a_y () (Bag Int))
; set semantics: a_y has no repeated element
(assert (= a_y (bag.setof a_y)))
(assert (bag.subbag a_y UNIVERALSET))
(assert (>= (bag.card a_y) (- n t)))


(assert (not (>= (* 2 (bag.card (bag.inter_min (bag.inter_min (bag.inter_min b_ba b_z) a_y) (bag.difference_subtract UNIVERALSET f)))) (+ (- n t) 1))))

(check-sat)
