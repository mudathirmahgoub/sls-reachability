(set-logic ALL)


; forall b_bt:B. forall a_bs:A. forall a_br:A. top(b_bt & a_bs & a_br)

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

(declare-fun b_bt () (Bag Int))
; set semantics: b_bt has no repeated element
(assert (= b_bt (bag.setof b_bt)))
(assert (bag.subbag b_bt UNIVERALSET))
(assert (>= (* 2 (bag.card b_bt)) (+ (+ n (* 3 t)) 1)))

(declare-fun a_bs () (Bag Int))
; set semantics: a_bs has no repeated element
(assert (= a_bs (bag.setof a_bs)))
(assert (bag.subbag a_bs UNIVERALSET))
(assert (>= (bag.card a_bs) (- n t)))

(declare-fun a_br () (Bag Int))
; set semantics: a_br has no repeated element
(assert (= a_br (bag.setof a_br)))
(assert (bag.subbag a_br UNIVERALSET))
(assert (>= (bag.card a_br) (- n t)))


(assert (>= (bag.card (bag.difference_subtract UNIVERALSET (bag.inter_min (bag.inter_min b_bt a_bs) a_br))) 1))

(check-sat)
