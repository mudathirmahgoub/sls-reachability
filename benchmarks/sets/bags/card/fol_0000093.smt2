(set-logic ALL)


; forall c_eb:C. forall b_ea:B. nonempty(c_eb & b_ea)

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

(declare-fun c_eb () (Bag Int))
; set semantics: c_eb has no repeated element
(assert (= c_eb (bag.setof c_eb)))
(assert (bag.subbag c_eb UNIVERALSET))
(assert (>= (* 2 (bag.card c_eb)) (+ (- n t) 1)))

(declare-fun b_ea () (Bag Int))
; set semantics: b_ea has no repeated element
(assert (= b_ea (bag.setof b_ea)))
(assert (bag.subbag b_ea UNIVERALSET))
(assert (>= (* 2 (bag.card b_ea)) (+ (+ n (* 3 t)) 1)))


(assert (= (bag.card (bag.inter_min c_eb b_ea)) 0))

(check-sat)
