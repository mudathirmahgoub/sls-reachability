(set-logic ALL)


; forall c_cc:C. nonempty(c_cc & ~f)

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

(declare-fun c_cc () (Bag Int))
; set semantics: c_cc has no repeated element
(assert (= c_cc (bag.setof c_cc)))
(assert (bag.subbag c_cc UNIVERALSET))
(assert (>= (* 2 (bag.card c_cc)) (+ (- n t) 1)))


(assert (= (bag.card (bag.inter_min c_cc (bag.difference_subtract UNIVERALSET f))) 0))

(check-sat)
