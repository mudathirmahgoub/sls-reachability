(set-logic ALL)


; forall b_bl:B. forall a_bk:A. B(b_bl & a_bk & ~f)

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

(declare-fun b_bl () (Bag Int))
; set semantics: b_bl has no repeated element
(assert (= b_bl (bag.setof b_bl)))
(assert (bag.subbag b_bl UNIVERALSET))
(assert (>= (* 2 (bag.card b_bl)) (+ (+ n (* 3 t)) 1)))

(declare-fun a_bk () (Bag Int))
; set semantics: a_bk has no repeated element
(assert (= a_bk (bag.setof a_bk)))
(assert (bag.subbag a_bk UNIVERALSET))
(assert (>= (bag.card a_bk) (- n t)))


(assert (not (>= (* 2 (bag.card (bag.inter_min (bag.inter_min b_bl a_bk) (bag.difference_subtract UNIVERALSET f)))) (+ (+ n (* 3 t)) 1))))

(check-sat)
