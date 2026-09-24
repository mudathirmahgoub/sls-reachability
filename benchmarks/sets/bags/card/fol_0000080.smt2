(set-logic ALL)


; forall b_df:B. forall b_de:B. B(b_df & b_de)

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

(declare-fun b_df () (Bag Int))
; set semantics: b_df has no repeated element
(assert (= b_df (bag.setof b_df)))
(assert (bag.subbag b_df UNIVERALSET))
(assert (>= (* 2 (bag.card b_df)) (+ (+ n (* 3 t)) 1)))

(declare-fun b_de () (Bag Int))
; set semantics: b_de has no repeated element
(assert (= b_de (bag.setof b_de)))
(assert (bag.subbag b_de UNIVERALSET))
(assert (>= (* 2 (bag.card b_de)) (+ (+ n (* 3 t)) 1)))


(assert (not (>= (* 2 (bag.card (bag.inter_min b_df b_de))) (+ (+ n (* 3 t)) 1))))

(check-sat)
