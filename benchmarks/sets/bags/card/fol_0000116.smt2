(set-logic ALL)


; forall b_gx:B. forall b_gw:B. forall a_gv:A. nonempty(b_gx & b_gw & a_gv)

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

(declare-fun b_gx () (Bag Int))
; set semantics: b_gx has no repeated element
(assert (= b_gx (bag.setof b_gx)))
(assert (bag.subbag b_gx UNIVERALSET))
(assert (>= (* 2 (bag.card b_gx)) (+ (+ n (* 3 t)) 1)))

(declare-fun b_gw () (Bag Int))
; set semantics: b_gw has no repeated element
(assert (= b_gw (bag.setof b_gw)))
(assert (bag.subbag b_gw UNIVERALSET))
(assert (>= (* 2 (bag.card b_gw)) (+ (+ n (* 3 t)) 1)))

(declare-fun a_gv () (Bag Int))
; set semantics: a_gv has no repeated element
(assert (= a_gv (bag.setof a_gv)))
(assert (bag.subbag a_gv UNIVERALSET))
(assert (>= (bag.card a_gv) (- n t)))


(assert (= (bag.card (bag.inter_min (bag.inter_min b_gx b_gw) a_gv)) 0))

(check-sat)
