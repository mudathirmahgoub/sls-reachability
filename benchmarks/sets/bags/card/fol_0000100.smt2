(set-logic ALL)


; forall c_ey:C. forall b_ex:B. forall b_ew:B. forall a_ev:A. forall a_eu:A. nonempty(c_ey & b_ex & b_ew & a_ev & a_eu & ~f)

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

(declare-fun c_ey () (Bag Int))
; set semantics: c_ey has no repeated element
(assert (= c_ey (bag.setof c_ey)))
(assert (bag.subbag c_ey UNIVERALSET))
(assert (>= (* 2 (bag.card c_ey)) (+ (- n t) 1)))

(declare-fun b_ex () (Bag Int))
; set semantics: b_ex has no repeated element
(assert (= b_ex (bag.setof b_ex)))
(assert (bag.subbag b_ex UNIVERALSET))
(assert (>= (* 2 (bag.card b_ex)) (+ (+ n (* 3 t)) 1)))

(declare-fun b_ew () (Bag Int))
; set semantics: b_ew has no repeated element
(assert (= b_ew (bag.setof b_ew)))
(assert (bag.subbag b_ew UNIVERALSET))
(assert (>= (* 2 (bag.card b_ew)) (+ (+ n (* 3 t)) 1)))

(declare-fun a_ev () (Bag Int))
; set semantics: a_ev has no repeated element
(assert (= a_ev (bag.setof a_ev)))
(assert (bag.subbag a_ev UNIVERALSET))
(assert (>= (bag.card a_ev) (- n t)))

(declare-fun a_eu () (Bag Int))
; set semantics: a_eu has no repeated element
(assert (= a_eu (bag.setof a_eu)))
(assert (bag.subbag a_eu UNIVERALSET))
(assert (>= (bag.card a_eu) (- n t)))


(assert (= (bag.card (bag.inter_min (bag.inter_min (bag.inter_min (bag.inter_min (bag.inter_min c_ey b_ex) b_ew) a_ev) a_eu) (bag.difference_subtract UNIVERALSET f))) 0))

(check-sat)
