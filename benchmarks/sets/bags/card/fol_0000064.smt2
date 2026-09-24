(set-logic ALL)


; forall c_bz:C. C(c_bz)

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

(declare-fun c_bz () (Bag Int))
; set semantics: c_bz has no repeated element
(assert (= c_bz (bag.setof c_bz)))
(assert (bag.subbag c_bz UNIVERALSET))
(assert (>= (* 2 (bag.card c_bz)) (+ (- n t) 1)))


(assert (not (>= (* 2 (bag.card c_bz)) (+ (- n t) 1))))

(check-sat)
