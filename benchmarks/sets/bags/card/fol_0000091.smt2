(set-logic ALL)


; forall c_dx:C. nonempty(c_dx)

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

(declare-fun c_dx () (Bag Int))
; set semantics: c_dx has no repeated element
(assert (= c_dx (bag.setof c_dx)))
(assert (bag.subbag c_dx UNIVERALSET))
(assert (>= (* 2 (bag.card c_dx)) (+ (- n t) 1)))


(assert (= (bag.card c_dx) 0))

(check-sat)
