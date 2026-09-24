(set-logic ALL)


; forall c_by:C. C(c_by & ~f)

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

(declare-fun c_by () (Bag Int))
; set semantics: c_by has no repeated element
(assert (= c_by (bag.setof c_by)))
(assert (bag.subbag c_by UNIVERALSET))
(assert (>= (* 2 (bag.card c_by)) (+ (- n t) 1)))


(assert (not (>= (* 2 (bag.card (bag.inter_min c_by (bag.difference_subtract UNIVERALSET f)))) (+ (- n t) 1))))

(check-sat)
