(set-logic ALL)


; forall c_gs:C. forall b_gr:B. nonempty(c_gs & b_gr)

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

(declare-fun c_gs () (Bag Int))
; set semantics: c_gs has no repeated element
(assert (= c_gs (bag.setof c_gs)))
(assert (bag.subbag c_gs UNIVERALSET))
(assert (>= (* 2 (bag.card c_gs)) (+ (- n t) 1)))

(declare-fun b_gr () (Bag Int))
; set semantics: b_gr has no repeated element
(assert (= b_gr (bag.setof b_gr)))
(assert (bag.subbag b_gr UNIVERALSET))
(assert (>= (* 2 (bag.card b_gr)) (+ (+ n (* 3 t)) 1)))


(assert (= (bag.card (bag.inter_min c_gs b_gr)) 0))

(check-sat)
