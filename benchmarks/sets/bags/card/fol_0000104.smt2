(set-logic ALL)


; forall c_fo:C. forall b_fn:B. forall a_fm:A. forall a_fl:A. nonempty(c_fo & b_fn & a_fm & a_fl & ~f)

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

(declare-fun c_fo () (Bag Int))
; set semantics: c_fo has no repeated element
(assert (= c_fo (bag.setof c_fo)))
(assert (bag.subbag c_fo UNIVERALSET))
(assert (>= (* 2 (bag.card c_fo)) (+ (- n t) 1)))

(declare-fun b_fn () (Bag Int))
; set semantics: b_fn has no repeated element
(assert (= b_fn (bag.setof b_fn)))
(assert (bag.subbag b_fn UNIVERALSET))
(assert (>= (* 2 (bag.card b_fn)) (+ (+ n (* 3 t)) 1)))

(declare-fun a_fm () (Bag Int))
; set semantics: a_fm has no repeated element
(assert (= a_fm (bag.setof a_fm)))
(assert (bag.subbag a_fm UNIVERALSET))
(assert (>= (bag.card a_fm) (- n t)))

(declare-fun a_fl () (Bag Int))
; set semantics: a_fl has no repeated element
(assert (= a_fl (bag.setof a_fl)))
(assert (bag.subbag a_fl UNIVERALSET))
(assert (>= (bag.card a_fl) (- n t)))


(assert (= (bag.card (bag.inter_min (bag.inter_min (bag.inter_min (bag.inter_min c_fo b_fn) a_fm) a_fl) (bag.difference_subtract UNIVERALSET f))) 0))

(check-sat)
