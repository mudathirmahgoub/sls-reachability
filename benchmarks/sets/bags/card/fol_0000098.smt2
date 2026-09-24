(set-logic ALL)


; forall b_eo:B. forall b_en:B. forall a_em:A. forall a_el:A. nonempty(b_eo & b_en & a_em & a_el & ~f)

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

(declare-fun b_eo () (Bag Int))
; set semantics: b_eo has no repeated element
(assert (= b_eo (bag.setof b_eo)))
(assert (bag.subbag b_eo UNIVERALSET))
(assert (>= (* 2 (bag.card b_eo)) (+ (+ n (* 3 t)) 1)))

(declare-fun b_en () (Bag Int))
; set semantics: b_en has no repeated element
(assert (= b_en (bag.setof b_en)))
(assert (bag.subbag b_en UNIVERALSET))
(assert (>= (* 2 (bag.card b_en)) (+ (+ n (* 3 t)) 1)))

(declare-fun a_em () (Bag Int))
; set semantics: a_em has no repeated element
(assert (= a_em (bag.setof a_em)))
(assert (bag.subbag a_em UNIVERALSET))
(assert (>= (bag.card a_em) (- n t)))

(declare-fun a_el () (Bag Int))
; set semantics: a_el has no repeated element
(assert (= a_el (bag.setof a_el)))
(assert (bag.subbag a_el UNIVERALSET))
(assert (>= (bag.card a_el) (- n t)))


(assert (= (bag.card (bag.inter_min (bag.inter_min (bag.inter_min (bag.inter_min b_eo b_en) a_em) a_el) (bag.difference_subtract UNIVERALSET f))) 0))

(check-sat)
