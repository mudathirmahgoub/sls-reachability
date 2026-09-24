(set-logic ALL)


; forall c_gq:C. forall b_gp:B. forall b_go:B. nonempty(c_gq & b_gp & b_go)

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

(declare-fun c_gq () (Bag Int))
; set semantics: c_gq has no repeated element
(assert (= c_gq (bag.setof c_gq)))
(assert (bag.subbag c_gq UNIVERALSET))
(assert (>= (* 2 (bag.card c_gq)) (+ (- n t) 1)))

(declare-fun b_gp () (Bag Int))
; set semantics: b_gp has no repeated element
(assert (= b_gp (bag.setof b_gp)))
(assert (bag.subbag b_gp UNIVERALSET))
(assert (>= (* 2 (bag.card b_gp)) (+ (+ n (* 3 t)) 1)))

(declare-fun b_go () (Bag Int))
; set semantics: b_go has no repeated element
(assert (= b_go (bag.setof b_go)))
(assert (bag.subbag b_go UNIVERALSET))
(assert (>= (* 2 (bag.card b_go)) (+ (+ n (* 3 t)) 1)))


(assert (= (bag.card (bag.inter_min (bag.inter_min c_gq b_gp) b_go)) 0))

(check-sat)
