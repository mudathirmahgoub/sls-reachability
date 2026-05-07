(set-logic HO_ALL)
(set-option :incremental true)
;---------------------
(declare-const x Int)
(declare-const y Int)
(assert 
(and 
  (= x 1)
  (= y 1)
(int.star-contains 
  (lambda ((x Int) (y Int)) (and (>= y (- 3 x)) (>= y (- x 3))))
  x y))
)
(check-sat)
