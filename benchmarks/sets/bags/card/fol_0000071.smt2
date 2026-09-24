(set-logic ALL)


; forall c_ck:C. forall b_cj:B. forall b_ci:B. nonempty(c_ck & b_cj & b_ci & ~f)

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

(declare-fun c_ck () (Bag Int))
; set semantics: c_ck has no repeated element
(assert (= c_ck (bag.setof c_ck)))
(assert (bag.subbag c_ck UNIVERALSET))
(assert (>= (* 2 (bag.card c_ck)) (+ (- n t) 1)))

(declare-fun b_cj () (Bag Int))
; set semantics: b_cj has no repeated element
(assert (= b_cj (bag.setof b_cj)))
(assert (bag.subbag b_cj UNIVERALSET))
(assert (>= (* 2 (bag.card b_cj)) (+ (+ n (* 3 t)) 1)))

(declare-fun b_ci () (Bag Int))
; set semantics: b_ci has no repeated element
(assert (= b_ci (bag.setof b_ci)))
(assert (bag.subbag b_ci UNIVERALSET))
(assert (>= (* 2 (bag.card b_ci)) (+ (+ n (* 3 t)) 1)))


(assert (= (bag.card (bag.inter_min (bag.inter_min (bag.inter_min c_ck b_cj) b_ci) (bag.difference_subtract UNIVERALSET f))) 0))

(check-sat)
