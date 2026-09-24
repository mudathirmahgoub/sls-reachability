(set-logic ALL)


; forall b_et:B. forall b_es:B. forall b_er:B. forall a_eq:A. forall a_ep:A. nonempty(b_et & b_es & b_er & a_eq & a_ep & ~f)

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

(declare-fun b_et () (Bag Int))
; set semantics: b_et has no repeated element
(assert (= b_et (bag.setof b_et)))
(assert (bag.subbag b_et UNIVERALSET))
(assert (>= (* 2 (bag.card b_et)) (+ (+ n (* 3 t)) 1)))

(declare-fun b_es () (Bag Int))
; set semantics: b_es has no repeated element
(assert (= b_es (bag.setof b_es)))
(assert (bag.subbag b_es UNIVERALSET))
(assert (>= (* 2 (bag.card b_es)) (+ (+ n (* 3 t)) 1)))

(declare-fun b_er () (Bag Int))
; set semantics: b_er has no repeated element
(assert (= b_er (bag.setof b_er)))
(assert (bag.subbag b_er UNIVERALSET))
(assert (>= (* 2 (bag.card b_er)) (+ (+ n (* 3 t)) 1)))

(declare-fun a_eq () (Bag Int))
; set semantics: a_eq has no repeated element
(assert (= a_eq (bag.setof a_eq)))
(assert (bag.subbag a_eq UNIVERALSET))
(assert (>= (bag.card a_eq) (- n t)))

(declare-fun a_ep () (Bag Int))
; set semantics: a_ep has no repeated element
(assert (= a_ep (bag.setof a_ep)))
(assert (bag.subbag a_ep UNIVERALSET))
(assert (>= (bag.card a_ep) (- n t)))


(assert (= (bag.card (bag.inter_min (bag.inter_min (bag.inter_min (bag.inter_min (bag.inter_min b_et b_es) b_er) a_eq) a_ep) (bag.difference_subtract UNIVERALSET f))) 0))

(check-sat)
