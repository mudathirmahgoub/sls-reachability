(set-logic ALL)


; forall b_ha:B. forall b_gz:B. forall b_gy:B. nonempty(b_ha & b_gz & b_gy)

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

(declare-fun b_ha () (Bag Int))
; set semantics: b_ha has no repeated element
(assert (= b_ha (bag.setof b_ha)))
(assert (bag.subbag b_ha UNIVERALSET))
(assert (>= (* 2 (bag.card b_ha)) (+ (+ n (* 3 t)) 1)))

(declare-fun b_gz () (Bag Int))
; set semantics: b_gz has no repeated element
(assert (= b_gz (bag.setof b_gz)))
(assert (bag.subbag b_gz UNIVERALSET))
(assert (>= (* 2 (bag.card b_gz)) (+ (+ n (* 3 t)) 1)))

(declare-fun b_gy () (Bag Int))
; set semantics: b_gy has no repeated element
(assert (= b_gy (bag.setof b_gy)))
(assert (bag.subbag b_gy UNIVERALSET))
(assert (>= (* 2 (bag.card b_gy)) (+ (+ n (* 3 t)) 1)))


(assert (= (bag.card (bag.inter_min (bag.inter_min b_ha b_gz) b_gy)) 0))

(check-sat)
