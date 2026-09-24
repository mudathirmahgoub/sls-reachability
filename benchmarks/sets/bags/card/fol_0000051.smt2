(set-logic ALL)


; forall b_bh:B. forall a_bg:A. A(b_bh & a_bg & ~f)

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

(declare-fun b_bh () (Bag Int))
; set semantics: b_bh has no repeated element
(assert (= b_bh (bag.setof b_bh)))
(assert (bag.subbag b_bh UNIVERALSET))
(assert (>= (* 2 (bag.card b_bh)) (+ (+ n (* 3 t)) 1)))

(declare-fun a_bg () (Bag Int))
; set semantics: a_bg has no repeated element
(assert (= a_bg (bag.setof a_bg)))
(assert (bag.subbag a_bg UNIVERALSET))
(assert (>= (bag.card a_bg) (- n t)))


(assert (not (>= (bag.card (bag.inter_min (bag.inter_min b_bh a_bg) (bag.difference_subtract UNIVERALSET f))) (- n t))))

(check-sat)
