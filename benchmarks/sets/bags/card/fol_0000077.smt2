(set-logic ALL)


; forall c_cx:C. forall b_cw:B. C(c_cx & b_cw & ~f)

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

(declare-fun c_cx () (Bag Int))
; set semantics: c_cx has no repeated element
(assert (= c_cx (bag.setof c_cx)))
(assert (bag.subbag c_cx UNIVERALSET))
(assert (>= (* 2 (bag.card c_cx)) (+ (- n t) 1)))

(declare-fun b_cw () (Bag Int))
; set semantics: b_cw has no repeated element
(assert (= b_cw (bag.setof b_cw)))
(assert (bag.subbag b_cw UNIVERALSET))
(assert (>= (* 2 (bag.card b_cw)) (+ (+ n (* 3 t)) 1)))


(assert (not (>= (* 2 (bag.card (bag.inter_min (bag.inter_min c_cx b_cw) (bag.difference_subtract UNIVERALSET f)))) (+ (- n t) 1))))

(check-sat)
