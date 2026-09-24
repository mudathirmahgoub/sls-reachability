(set-logic ALL)


; forall c_cv:C. forall b_cu:B. B(c_cv & b_cu & ~f)

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

(declare-fun c_cv () (Bag Int))
; set semantics: c_cv has no repeated element
(assert (= c_cv (bag.setof c_cv)))
(assert (bag.subbag c_cv UNIVERALSET))
(assert (>= (* 2 (bag.card c_cv)) (+ (- n t) 1)))

(declare-fun b_cu () (Bag Int))
; set semantics: b_cu has no repeated element
(assert (= b_cu (bag.setof b_cu)))
(assert (bag.subbag b_cu UNIVERALSET))
(assert (>= (* 2 (bag.card b_cu)) (+ (+ n (* 3 t)) 1)))


(assert (not (>= (* 2 (bag.card (bag.inter_min (bag.inter_min c_cv b_cu) (bag.difference_subtract UNIVERALSET f)))) (+ (+ n (* 3 t)) 1))))

(check-sat)
