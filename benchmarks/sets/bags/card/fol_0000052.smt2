(set-logic ALL)


; forall c_bj:C. forall b_bi:B. C(c_bj & b_bi & ~f)

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

(declare-fun c_bj () (Bag Int))
; set semantics: c_bj has no repeated element
(assert (= c_bj (bag.setof c_bj)))
(assert (bag.subbag c_bj UNIVERALSET))
(assert (>= (* 2 (bag.card c_bj)) (+ (- n t) 1)))

(declare-fun b_bi () (Bag Int))
; set semantics: b_bi has no repeated element
(assert (= b_bi (bag.setof b_bi)))
(assert (bag.subbag b_bi UNIVERALSET))
(assert (>= (* 2 (bag.card b_bi)) (+ (+ n (* 3 t)) 1)))


(assert (not (>= (* 2 (bag.card (bag.inter_min (bag.inter_min c_bj b_bi) (bag.difference_subtract UNIVERALSET f)))) (+ (- n t) 1))))

(check-sat)
