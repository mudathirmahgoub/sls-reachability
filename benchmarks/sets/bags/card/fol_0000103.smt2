(set-logic ALL)


; forall b_fk:B. forall b_fj:B. forall a_fi:A. forall a_fh:A. A(b_fk & b_fj & a_fi & a_fh & ~f)

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

(declare-fun b_fk () (Bag Int))
; set semantics: b_fk has no repeated element
(assert (= b_fk (bag.setof b_fk)))
(assert (bag.subbag b_fk UNIVERALSET))
(assert (>= (* 2 (bag.card b_fk)) (+ (+ n (* 3 t)) 1)))

(declare-fun b_fj () (Bag Int))
; set semantics: b_fj has no repeated element
(assert (= b_fj (bag.setof b_fj)))
(assert (bag.subbag b_fj UNIVERALSET))
(assert (>= (* 2 (bag.card b_fj)) (+ (+ n (* 3 t)) 1)))

(declare-fun a_fi () (Bag Int))
; set semantics: a_fi has no repeated element
(assert (= a_fi (bag.setof a_fi)))
(assert (bag.subbag a_fi UNIVERALSET))
(assert (>= (bag.card a_fi) (- n t)))

(declare-fun a_fh () (Bag Int))
; set semantics: a_fh has no repeated element
(assert (= a_fh (bag.setof a_fh)))
(assert (bag.subbag a_fh UNIVERALSET))
(assert (>= (bag.card a_fh) (- n t)))


(assert (not (>= (bag.card (bag.inter_min (bag.inter_min (bag.inter_min (bag.inter_min b_fk b_fj) a_fi) a_fh) (bag.difference_subtract UNIVERALSET f))) (- n t))))

(check-sat)
