(set-logic ALL)


; forall b_dk:B. forall b_dj:B. nonempty(b_dk & b_dj)

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

(declare-fun b_dk () (Bag Int))
; set semantics: b_dk has no repeated element
(assert (= b_dk (bag.setof b_dk)))
(assert (bag.subbag b_dk UNIVERALSET))
(assert (>= (* 2 (bag.card b_dk)) (+ (+ n (* 3 t)) 1)))

(declare-fun b_dj () (Bag Int))
; set semantics: b_dj has no repeated element
(assert (= b_dj (bag.setof b_dj)))
(assert (bag.subbag b_dj UNIVERALSET))
(assert (>= (* 2 (bag.card b_dj)) (+ (+ n (* 3 t)) 1)))


(assert (= (bag.card (bag.inter_min b_dk b_dj)) 0))

(check-sat)
