(set-logic ALL)


; forall c_dw:C. forall c_dv:C. nonempty(c_dw & c_dv)

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

(declare-fun c_dw () (Bag Int))
; set semantics: c_dw has no repeated element
(assert (= c_dw (bag.setof c_dw)))
(assert (bag.subbag c_dw UNIVERALSET))
(assert (>= (* 2 (bag.card c_dw)) (+ (- n t) 1)))

(declare-fun c_dv () (Bag Int))
; set semantics: c_dv has no repeated element
(assert (= c_dv (bag.setof c_dv)))
(assert (bag.subbag c_dv UNIVERALSET))
(assert (>= (* 2 (bag.card c_dv)) (+ (- n t) 1)))


(assert (= (bag.card (bag.inter_min c_dw c_dv)) 0))

(check-sat)
