(set-logic ALL)


; forall c_cp:C. forall b_co:B. nonempty(c_cp & b_co & f & ~f)

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

(declare-fun c_cp () (Bag Int))
; set semantics: c_cp has no repeated element
(assert (= c_cp (bag.setof c_cp)))
(assert (bag.subbag c_cp UNIVERALSET))
(assert (>= (* 2 (bag.card c_cp)) (+ (- n t) 1)))

(declare-fun b_co () (Bag Int))
; set semantics: b_co has no repeated element
(assert (= b_co (bag.setof b_co)))
(assert (bag.subbag b_co UNIVERALSET))
(assert (>= (* 2 (bag.card b_co)) (+ (+ n (* 3 t)) 1)))


(assert (= (bag.card (bag.inter_min (bag.inter_min (bag.inter_min c_cp b_co) f) (bag.difference_subtract UNIVERALSET f))) 0))

(check-sat)
