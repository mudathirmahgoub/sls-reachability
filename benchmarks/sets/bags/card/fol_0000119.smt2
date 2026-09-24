(set-logic ALL)


; forall a_hf:A. forall a_he:A. nonempty(a_hf & a_he & ~f)

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

(declare-fun a_hf () (Bag Int))
; set semantics: a_hf has no repeated element
(assert (= a_hf (bag.setof a_hf)))
(assert (bag.subbag a_hf UNIVERALSET))
(assert (>= (bag.card a_hf) (- n t)))

(declare-fun a_he () (Bag Int))
; set semantics: a_he has no repeated element
(assert (= a_he (bag.setof a_he)))
(assert (bag.subbag a_he UNIVERALSET))
(assert (>= (bag.card a_he) (- n t)))


(assert (= (bag.card (bag.inter_min (bag.inter_min a_hf a_he) (bag.difference_subtract UNIVERALSET f))) 0))

(check-sat)
