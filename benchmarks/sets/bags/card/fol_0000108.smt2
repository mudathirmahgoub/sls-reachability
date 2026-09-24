(set-logic ALL)


; forall b_gg:B. forall b_gf:B. forall a_ge:A. forall a_gd:A. forall a_gc:A. top(b_gg & b_gf & a_ge & a_gd & a_gc)

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

(declare-fun b_gg () (Bag Int))
; set semantics: b_gg has no repeated element
(assert (= b_gg (bag.setof b_gg)))
(assert (bag.subbag b_gg UNIVERALSET))
(assert (>= (* 2 (bag.card b_gg)) (+ (+ n (* 3 t)) 1)))

(declare-fun b_gf () (Bag Int))
; set semantics: b_gf has no repeated element
(assert (= b_gf (bag.setof b_gf)))
(assert (bag.subbag b_gf UNIVERALSET))
(assert (>= (* 2 (bag.card b_gf)) (+ (+ n (* 3 t)) 1)))

(declare-fun a_ge () (Bag Int))
; set semantics: a_ge has no repeated element
(assert (= a_ge (bag.setof a_ge)))
(assert (bag.subbag a_ge UNIVERALSET))
(assert (>= (bag.card a_ge) (- n t)))

(declare-fun a_gd () (Bag Int))
; set semantics: a_gd has no repeated element
(assert (= a_gd (bag.setof a_gd)))
(assert (bag.subbag a_gd UNIVERALSET))
(assert (>= (bag.card a_gd) (- n t)))

(declare-fun a_gc () (Bag Int))
; set semantics: a_gc has no repeated element
(assert (= a_gc (bag.setof a_gc)))
(assert (bag.subbag a_gc UNIVERALSET))
(assert (>= (bag.card a_gc) (- n t)))


(assert (>= (bag.card (bag.difference_subtract UNIVERALSET (bag.inter_min (bag.inter_min (bag.inter_min (bag.inter_min b_gg b_gf) a_ge) a_gd) a_gc))) 1))

(check-sat)
