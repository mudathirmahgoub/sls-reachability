(set-logic ALL)


; forall b_gb:B. forall b_ga:B. forall a_fz:A. forall a_fy:A. forall a_fx:A. nonempty(b_gb & b_ga & a_fz & a_fy & a_fx)

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

(declare-fun b_gb () (Bag Int))
; set semantics: b_gb has no repeated element
(assert (= b_gb (bag.setof b_gb)))
(assert (bag.subbag b_gb UNIVERALSET))
(assert (>= (* 2 (bag.card b_gb)) (+ (+ n (* 3 t)) 1)))

(declare-fun b_ga () (Bag Int))
; set semantics: b_ga has no repeated element
(assert (= b_ga (bag.setof b_ga)))
(assert (bag.subbag b_ga UNIVERALSET))
(assert (>= (* 2 (bag.card b_ga)) (+ (+ n (* 3 t)) 1)))

(declare-fun a_fz () (Bag Int))
; set semantics: a_fz has no repeated element
(assert (= a_fz (bag.setof a_fz)))
(assert (bag.subbag a_fz UNIVERALSET))
(assert (>= (bag.card a_fz) (- n t)))

(declare-fun a_fy () (Bag Int))
; set semantics: a_fy has no repeated element
(assert (= a_fy (bag.setof a_fy)))
(assert (bag.subbag a_fy UNIVERALSET))
(assert (>= (bag.card a_fy) (- n t)))

(declare-fun a_fx () (Bag Int))
; set semantics: a_fx has no repeated element
(assert (= a_fx (bag.setof a_fx)))
(assert (bag.subbag a_fx UNIVERALSET))
(assert (>= (bag.card a_fx) (- n t)))


(assert (= (bag.card (bag.inter_min (bag.inter_min (bag.inter_min (bag.inter_min b_gb b_ga) a_fz) a_fy) a_fx)) 0))

(check-sat)
