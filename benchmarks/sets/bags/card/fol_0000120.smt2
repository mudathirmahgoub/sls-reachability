(set-logic ALL)


; forall a_hi:A. forall a_hh:A. forall a_hg:A. nonempty(a_hi & a_hh & a_hg)

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

(declare-fun a_hi () (Bag Int))
; set semantics: a_hi has no repeated element
(assert (= a_hi (bag.setof a_hi)))
(assert (bag.subbag a_hi UNIVERALSET))
(assert (>= (bag.card a_hi) (- n t)))

(declare-fun a_hh () (Bag Int))
; set semantics: a_hh has no repeated element
(assert (= a_hh (bag.setof a_hh)))
(assert (bag.subbag a_hh UNIVERALSET))
(assert (>= (bag.card a_hh) (- n t)))

(declare-fun a_hg () (Bag Int))
; set semantics: a_hg has no repeated element
(assert (= a_hg (bag.setof a_hg)))
(assert (bag.subbag a_hg UNIVERALSET))
(assert (>= (bag.card a_hg) (- n t)))


(assert (= (bag.card (bag.inter_min (bag.inter_min a_hi a_hh) a_hg)) 0))

(check-sat)
