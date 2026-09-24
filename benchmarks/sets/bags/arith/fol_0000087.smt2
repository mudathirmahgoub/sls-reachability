(set-logic ALL)


; forall c_dg:C. forall a_df:A. c_dg + a_df + |UNIVERALSET| - 2n >= 1 or 1 <= 0

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

(declare-fun c_dg () Int)
(assert (<= c_dg n))
(assert (>= c_dg 0))
(assert (>= (* 2 c_dg) (+ (- n t) 1)))

(declare-fun a_df () Int)
(assert (<= a_df n))
(assert (>= a_df 0))
(assert (>= a_df (- n t)))


(assert (and (< (- (+ (+ c_dg a_df) (bag.card UNIVERALSET)) (* 2 n)) 1) (> 1 0)))

(check-sat)
