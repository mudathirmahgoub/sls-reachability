(set-logic ALL)


; forall a_ex:A. 2a_ex + |~f| - 2n >= 1 or 1 <= 0

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

(declare-fun a_ex () Int)
(assert (<= a_ex n))
(assert (>= a_ex 0))
(assert (>= a_ex (- n t)))


(assert (and (< (- (+ (* 2 a_ex) (bag.card (bag.difference_subtract UNIVERALSET f))) (* 2 n)) 1) (> 1 0)))

(check-sat)
