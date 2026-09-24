(set-logic ALL)


; forall c_dq:C. forall a_dp:A. nonempty(c_dq & a_dp)

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

(declare-fun c_dq () (Bag Int))
; set semantics: c_dq has no repeated element
(assert (= c_dq (bag.setof c_dq)))
(assert (bag.subbag c_dq UNIVERALSET))
(assert (>= (* 2 (bag.card c_dq)) (+ (- n t) 1)))

(declare-fun a_dp () (Bag Int))
; set semantics: a_dp has no repeated element
(assert (= a_dp (bag.setof a_dp)))
(assert (bag.subbag a_dp UNIVERALSET))
(assert (>= (bag.card a_dp) (- n t)))


(assert (= (bag.card (bag.inter_min c_dq a_dp)) 0))

(check-sat)
