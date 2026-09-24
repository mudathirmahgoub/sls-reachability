(set-logic ALL)


; forall a_d:A. a_d + |UNIVERALSET| - n >= (n - t + 1) / 2 or (n - t + 1) / 2 <= 0

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

(declare-fun a_d () Int)
(assert (<= a_d n))
(assert (>= a_d 0))
(assert (>= a_d (- n t)))


(assert (and (< (* 2 (- (+ a_d (bag.card UNIVERALSET)) n)) (+ (- n t) 1)) (> (+ (- n t) 1) (* 2 0))))

(check-sat)
