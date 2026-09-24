(set-logic ALL)


; forall b_fw:B. forall b_fv:B. forall a_fu:A. forall a_ft:A. C(b_fw & b_fv & a_fu & a_ft & ~f)

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

(declare-fun b_fw () (Bag Int))
; set semantics: b_fw has no repeated element
(assert (= b_fw (bag.setof b_fw)))
(assert (bag.subbag b_fw UNIVERALSET))
(assert (>= (* 2 (bag.card b_fw)) (+ (+ n (* 3 t)) 1)))

(declare-fun b_fv () (Bag Int))
; set semantics: b_fv has no repeated element
(assert (= b_fv (bag.setof b_fv)))
(assert (bag.subbag b_fv UNIVERALSET))
(assert (>= (* 2 (bag.card b_fv)) (+ (+ n (* 3 t)) 1)))

(declare-fun a_fu () (Bag Int))
; set semantics: a_fu has no repeated element
(assert (= a_fu (bag.setof a_fu)))
(assert (bag.subbag a_fu UNIVERALSET))
(assert (>= (bag.card a_fu) (- n t)))

(declare-fun a_ft () (Bag Int))
; set semantics: a_ft has no repeated element
(assert (= a_ft (bag.setof a_ft)))
(assert (bag.subbag a_ft UNIVERALSET))
(assert (>= (bag.card a_ft) (- n t)))


(assert (not (>= (* 2 (bag.card (bag.inter_min (bag.inter_min (bag.inter_min (bag.inter_min b_fw b_fv) a_fu) a_ft) (bag.difference_subtract UNIVERALSET f)))) (+ (- n t) 1))))

(check-sat)
