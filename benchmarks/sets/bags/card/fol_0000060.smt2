(set-logic ALL)


; forall a_bw:A. C(a_bw & ~f)

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

(declare-fun a_bw () (Bag Int))
; set semantics: a_bw has no repeated element
(assert (= a_bw (bag.setof a_bw)))
(assert (bag.subbag a_bw UNIVERALSET))
(assert (>= (bag.card a_bw) (- n t)))


(assert (not (>= (* 2 (bag.card (bag.inter_min a_bw (bag.difference_subtract UNIVERALSET f)))) (+ (- n t) 1))))

(check-sat)
