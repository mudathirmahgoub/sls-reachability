(set-logic ALL)


; forall c_cf:C. forall a_ce:A. nonempty(c_cf & a_ce & ~f)

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

(declare-fun c_cf () (Bag Int))
; set semantics: c_cf has no repeated element
(assert (= c_cf (bag.setof c_cf)))
(assert (bag.subbag c_cf UNIVERALSET))
(assert (>= (* 2 (bag.card c_cf)) (+ (- n t) 1)))

(declare-fun a_ce () (Bag Int))
; set semantics: a_ce has no repeated element
(assert (= a_ce (bag.setof a_ce)))
(assert (bag.subbag a_ce UNIVERALSET))
(assert (>= (bag.card a_ce) (- n t)))


(assert (= (bag.card (bag.inter_min (bag.inter_min c_cf a_ce) (bag.difference_subtract UNIVERALSET f))) 0))

(check-sat)
