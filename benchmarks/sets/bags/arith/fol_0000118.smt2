(set-logic ALL)


; forall a_fg:A. 3a_fg + |~f| - 3n >= 1 or 1 <= 0

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

(declare-fun a_fg () Int)
(assert (<= a_fg n))
(assert (>= a_fg 0))
(assert (>= a_fg (- n t)))


(assert (and (< (- (+ (* 3 a_fg) (bag.card (bag.difference_subtract UNIVERALSET f))) (* 3 n)) 1) (> 1 0)))

(check-sat)
