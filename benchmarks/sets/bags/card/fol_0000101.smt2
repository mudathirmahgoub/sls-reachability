(set-logic ALL)


; forall b_fc:B. forall b_fb:B. forall a_fa:A. forall a_ez:A. nonempty(b_fc & b_fb & a_fa & a_ez & f & ~f)

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

(declare-fun b_fc () (Bag Int))
; set semantics: b_fc has no repeated element
(assert (= b_fc (bag.setof b_fc)))
(assert (bag.subbag b_fc UNIVERALSET))
(assert (>= (* 2 (bag.card b_fc)) (+ (+ n (* 3 t)) 1)))

(declare-fun b_fb () (Bag Int))
; set semantics: b_fb has no repeated element
(assert (= b_fb (bag.setof b_fb)))
(assert (bag.subbag b_fb UNIVERALSET))
(assert (>= (* 2 (bag.card b_fb)) (+ (+ n (* 3 t)) 1)))

(declare-fun a_fa () (Bag Int))
; set semantics: a_fa has no repeated element
(assert (= a_fa (bag.setof a_fa)))
(assert (bag.subbag a_fa UNIVERALSET))
(assert (>= (bag.card a_fa) (- n t)))

(declare-fun a_ez () (Bag Int))
; set semantics: a_ez has no repeated element
(assert (= a_ez (bag.setof a_ez)))
(assert (bag.subbag a_ez UNIVERALSET))
(assert (>= (bag.card a_ez) (- n t)))


(assert (= (bag.card (bag.inter_min (bag.inter_min (bag.inter_min (bag.inter_min (bag.inter_min b_fc b_fb) a_fa) a_ez) f) (bag.difference_subtract UNIVERALSET f))) 0))

(check-sat)
