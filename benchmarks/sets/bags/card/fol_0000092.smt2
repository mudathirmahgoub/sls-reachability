(set-logic ALL)


; forall c_dz:C. forall a_dy:A. nonempty(c_dz & a_dy)

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

(declare-fun c_dz () (Bag Int))
; set semantics: c_dz has no repeated element
(assert (= c_dz (bag.setof c_dz)))
(assert (bag.subbag c_dz UNIVERALSET))
(assert (>= (* 2 (bag.card c_dz)) (+ (- n t) 1)))

(declare-fun a_dy () (Bag Int))
; set semantics: a_dy has no repeated element
(assert (= a_dy (bag.setof a_dy)))
(assert (bag.subbag a_dy UNIVERALSET))
(assert (>= (bag.card a_dy) (- n t)))


(assert (= (bag.card (bag.inter_min c_dz a_dy)) 0))

(check-sat)
