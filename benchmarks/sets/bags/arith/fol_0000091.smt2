(set-logic ALL)


; forall c_dl:C. c_dl + |UNIVERALSET| - n >= 1 or 1 <= 0

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

(declare-fun c_dl () Int)
(assert (<= c_dl n))
(assert (>= c_dl 0))
(assert (>= (* 2 c_dl) (+ (- n t) 1)))


(assert (and (< (- (+ c_dl (bag.card UNIVERALSET)) n) 1) (> 1 0)))

(check-sat)
