(set-logic ALL)


; forall c_dd:C. forall b_dc:B. forall a_db:A. top(c_dd & b_dc & a_db)

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

(declare-fun c_dd () (Bag Int))
; set semantics: c_dd has no repeated element
(assert (= c_dd (bag.setof c_dd)))
(assert (bag.subbag c_dd UNIVERALSET))
(assert (>= (* 2 (bag.card c_dd)) (+ (- n t) 1)))

(declare-fun b_dc () (Bag Int))
; set semantics: b_dc has no repeated element
(assert (= b_dc (bag.setof b_dc)))
(assert (bag.subbag b_dc UNIVERALSET))
(assert (>= (* 2 (bag.card b_dc)) (+ (+ n (* 3 t)) 1)))

(declare-fun a_db () (Bag Int))
; set semantics: a_db has no repeated element
(assert (= a_db (bag.setof a_db)))
(assert (bag.subbag a_db UNIVERALSET))
(assert (>= (bag.card a_db) (- n t)))


(assert (>= (bag.card (bag.difference_subtract UNIVERALSET (bag.inter_min (bag.inter_min c_dd b_dc) a_db))) 1))

(check-sat)
