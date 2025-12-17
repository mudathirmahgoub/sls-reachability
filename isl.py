import islpy as isl

s = isl.Set("[x,y] -> { [x,y] : y >= 5 - x and x <= 5 + y }")
simplified = s.coalesce()

bs_list = simplified.get_basic_set_list()
for i in range(bs_list.n_basic_set()):
    bs = bs_list.get_basic_set(i)
    print("Basic set", i, ":", bs)

    for c in bs.get_constraints():
        print("   constraint:", c)
    
    
    pt = bs.sample_point()
    print("Sample point:", pt)
    bounded = bs.intersect(isl.Set("[x,y] -> { [x,y] : 0 <= x,y <= 10 }"))
    it = bounded.points()
    while not it.is_empty():
      print("Point:", it.get_point())
      it = it.next()
