(set-logic ALL)


; forall c_cd:C. nonempty(c_cd & ~f)

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

(declare-fun c_cd () (Bag Int))
; set semantics: c_cd has no repeated element
(assert (= c_cd (bag.setof c_cd)))
(assert (bag.subbag c_cd UNIVERALSET))
(assert (>= (* 2 (bag.card c_cd)) (+ (- n t) 1)))


(assert (= (bag.card (bag.inter_min c_cd (bag.difference_subtract UNIVERALSET f))) 0))

(check-sat)
