(set-logic ALL)


; forall b_gu:B. forall b_gt:B. nonempty(b_gu & b_gt)

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

(declare-fun b_gu () (Bag Int))
; set semantics: b_gu has no repeated element
(assert (= b_gu (bag.setof b_gu)))
(assert (bag.subbag b_gu UNIVERALSET))
(assert (>= (* 2 (bag.card b_gu)) (+ (+ n (* 3 t)) 1)))

(declare-fun b_gt () (Bag Int))
; set semantics: b_gt has no repeated element
(assert (= b_gt (bag.setof b_gt)))
(assert (bag.subbag b_gt UNIVERALSET))
(assert (>= (* 2 (bag.card b_gt)) (+ (+ n (* 3 t)) 1)))


(assert (= (bag.card (bag.inter_min b_gu b_gt)) 0))

(check-sat)
