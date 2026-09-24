(set-logic ALL)


; forall a_gl:A. forall a_gk:A. C(a_gl & a_gk)

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

(declare-fun a_gl () (Bag Int))
; set semantics: a_gl has no repeated element
(assert (= a_gl (bag.setof a_gl)))
(assert (bag.subbag a_gl UNIVERALSET))
(assert (>= (bag.card a_gl) (- n t)))

(declare-fun a_gk () (Bag Int))
; set semantics: a_gk has no repeated element
(assert (= a_gk (bag.setof a_gk)))
(assert (bag.subbag a_gk UNIVERALSET))
(assert (>= (bag.card a_gk) (- n t)))


(assert (not (>= (* 2 (bag.card (bag.inter_min a_gl a_gk))) (+ (- n t) 1))))

(check-sat)
