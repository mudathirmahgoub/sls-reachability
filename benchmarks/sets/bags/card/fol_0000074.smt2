(set-logic ALL)


; forall c_cr:C. forall b_cq:B. A(c_cr & b_cq & ~f)

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

(declare-fun c_cr () (Bag Int))
; set semantics: c_cr has no repeated element
(assert (= c_cr (bag.setof c_cr)))
(assert (bag.subbag c_cr UNIVERALSET))
(assert (>= (* 2 (bag.card c_cr)) (+ (- n t) 1)))

(declare-fun b_cq () (Bag Int))
; set semantics: b_cq has no repeated element
(assert (= b_cq (bag.setof b_cq)))
(assert (bag.subbag b_cq UNIVERALSET))
(assert (>= (* 2 (bag.card b_cq)) (+ (+ n (* 3 t)) 1)))


(assert (not (>= (bag.card (bag.inter_min (bag.inter_min c_cr b_cq) (bag.difference_subtract UNIVERALSET f))) (- n t))))

(check-sat)
