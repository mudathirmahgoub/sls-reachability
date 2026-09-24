(set-logic ALL)


; forall a_n:A. a_n + |UNIVERALSET| - n >= n or n <= 0

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

(declare-fun a_n () Int)
(assert (<= a_n n))
(assert (>= a_n 0))
(assert (>= a_n (- n t)))


(assert (and (< (- (+ a_n (bag.card UNIVERALSET)) n) n) (> n 0)))

(check-sat)
