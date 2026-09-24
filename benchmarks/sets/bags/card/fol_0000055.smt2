(set-logic ALL)


; forall b_bq:B. forall a_bp:A. forall a_bo:A. C(b_bq & a_bp & a_bo)

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

(declare-fun b_bq () (Bag Int))
; set semantics: b_bq has no repeated element
(assert (= b_bq (bag.setof b_bq)))
(assert (bag.subbag b_bq UNIVERALSET))
(assert (>= (* 2 (bag.card b_bq)) (+ (+ n (* 3 t)) 1)))

(declare-fun a_bp () (Bag Int))
; set semantics: a_bp has no repeated element
(assert (= a_bp (bag.setof a_bp)))
(assert (bag.subbag a_bp UNIVERALSET))
(assert (>= (bag.card a_bp) (- n t)))

(declare-fun a_bo () (Bag Int))
; set semantics: a_bo has no repeated element
(assert (= a_bo (bag.setof a_bo)))
(assert (bag.subbag a_bo UNIVERALSET))
(assert (>= (bag.card a_bo) (- n t)))


(assert (not (>= (* 2 (bag.card (bag.inter_min (bag.inter_min b_bq a_bp) a_bo))) (+ (- n t) 1))))

(check-sat)
