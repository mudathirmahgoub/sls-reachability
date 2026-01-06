from ppl import Variable, Constraint_System, C_Polyhedron,NNC_Polyhedron

import unittest



           
            
def print_generators(p):
     # Inspect generators (vertices and rays)
    gens = p.minimized_generators()
    for g in gens:
        print("Generator:", g)


class TestPPL(unittest.TestCase):

    def test_formula_simple(self): 
        # Define variables x=0, y=1
        x = Variable(0)
        y = Variable(1)

        # Build constraint system: y >= 5 - x and x <= 5 + y
        cs = Constraint_System()

        cs.insert(x >= 0)
        cs.insert(y >= 0)
        cs.insert(y >= 5 - x)
        cs.insert(x <= 5 + y)

        # Create polyhedron
        ph = NNC_Polyhedron(cs)

        print("Polyhedron:", ph)

        # Inspect generators (vertices and rays)
        gens = ph.minimized_generators()
        for g in gens:
            print("Generator:", g)

    def test_f1(self): 
         # Define variables x=0, y=1
        x = Variable(0)
        y = Variable(1)

        # Build constraint system: y >= 5 - x and x <= 5 + y
        cs = Constraint_System()
        cs.insert(x >= 0)
        cs.insert(y >= 0)

        cs.insert(y + 2 * x >= 17)
        cs.insert(6*x - y <= 47)
        
        # Create polyhedron
        ph = NNC_Polyhedron(cs)

        print(f'is_bounded: {ph.is_bounded()}')

        print("Polyhedron:", ph)

        # Inspect generators (vertices and rays)
        gens = ph.minimized_generators()
        for g in gens:
            print("Generator:", g)


    def test_f2(self): 
        x = Variable(0)
        y = Variable(1)

        # Build constraint system: y >= 5 - x and x <= 5 + y
        cs = Constraint_System()
        cs.insert(x >= 0)
        cs.insert(y >= 0)
        cs.insert(5*x + 2*y >= 17)
        cs.insert(3*x - y <= 8)
        cs.insert(2*x + 3*y <= 20)

        # Create polyhedron
        ph = NNC_Polyhedron(cs)

        print("Polyhedron:", ph)
        print(f'is_bounded: {ph.is_bounded()}')

        # Inspect generators (vertices and rays)
        gens = ph.minimized_generators()
        for g in gens:
            print("Generator:", g)


    def test_mapa(self): 
        # Define variables x=0, y=1
        x = Variable(0)
        y = Variable(1)
        z = Variable(2)    

        cs = Constraint_System()
        cs.insert(x >= 0)
        cs.insert(y >= 0)
        cs.insert(z >= 0)
          
        cs.insert(x ==  y - z)
        cs.insert(z <= x)
        

        # Create polyhedron
        ph = C_Polyhedron(cs)

        print("Polyhedron:", ph)

        # Inspect generators (vertices and rays)
        gens = ph.minimized_generators()
        for g in gens:
            print("Generator:", g)

        # exists l1, l2 . x1 = l1 and x2 = l1 + l2 and x3 = l3
        # exists l1 l2 . x1 = l1 + l2 and x2 = l1  + 2 * l2 and x3 = l3

        # x2 = l1 + l2 => x2 = x1 + l2
        # x1 = l1 

        # x2 = l1 + 2 * l2  => x2 = x1 + l1
        # x1 = l1 + l2

    def test_integer(self): 
        # Define variables x=0, y=1
        x = Variable(0)
        y = Variable(1)
        cs = Constraint_System()
        cs.insert(4*x >= 1)
        cs.insert(4 *y >= 1)
          
        cs.insert(2 * x <= 1)  
        cs.insert(2 * y <= 1)        

        # Create polyhedron
        ph = C_Polyhedron(cs)

        print(f"Polyhedron:{ph}", ph)

        print(f'is_empty: {ph.is_empty()}')
        print(f'is_bounded: {ph.is_bounded()}')
        print(f'has integers: {ph.contains_integer_point()}')
        print(f'is_universe: {ph.is_universe()}')
        print(f'is_topologically_closed: {ph.is_topologically_closed()}')

        # Inspect generators (vertices and rays)
        gens = ph.minimized_generators()
        for g in gens:
            print("Generator:", g)

        # exists l1, l2 . x1 = l1 and x2 = l1 + l2 and x3 = l3
        # exists l1 l2 . x1 = l1 + l2 and x2 = l1  + 2 * l2 and x3 = l3

        # x2 = l1 + l2 => x2 = x1 + l2
        # x1 = l1 

        # x2 = l1 + 2 * l2  => x2 = x1 + l1
        # x1 = l1 + l2


    def test_unsat(self): 
            # Define variables x=0, y=1
            x1, L, x, z1, z2 = (Variable(0),Variable(1),Variable(2),Variable(3),Variable(4))
            cs = Constraint_System()
            cs.insert(x1 >= 0)
            cs.insert(L >= 0)
            cs.insert(x >= 0)
            cs.insert(z1 >= 0)
            cs.insert(z2 >= 0)
            
            # A1 = {(0, 0, 0, 0, 0)}, B1 = {(0, 1, 1, 0, 0)}
            print("----------------------------")
            print("p1")
            p1 = C_Polyhedron(cs)
            p1.add_constraint(x <= L)
            p1.add_constraint(z2 == 0)
            p1.add_constraint(L <= x)
            p1.add_constraint(x1 == 0)
            p1.add_constraint(z1 == 0)                       
            print_generators(p1)
            print(f"contains integers: {p1.contains_integer_point()}")
            print("----------------------------")
            # A3 = {(0, 0, 1, 0, 1)}, B3 = {(0, 1, 1, 0, 0), (0, 0, 1, 0, 0)}
            print("p2")
            p2 = C_Polyhedron(cs)
            p2.add_constraint(x >= L + 1)
            p2.add_constraint(z2 == 1)
            p2.add_constraint(L <= x)
            p2.add_constraint(x1 == 0)
            p2.add_constraint(z1 == 0)                       
            print_generators(p2)
            print(f"contains integers: {p2.contains_integer_point()}")
            print("----------------------------")
            print("p3") 
            # A5 = {(1, 1, 0, 0, 0)}, B5 = {(1, 1, 0, 0, 0), (0, 1, 1, 0, 0)}
            p3 = C_Polyhedron(cs)
            p3.add_constraint(x <= L)
            p3.add_constraint(z2 == 0)
            p3.add_constraint(L >= x + 1)
            p3.add_constraint(x1 == L  - x)
            p3.add_constraint(z1 == 0)                       
            print_generators(p3)
            print(f"contains integers: {p3.contains_integer_point()}")
            #
            print("----------------------------")
            print("p4") 
            # A5 = {(1, 1, 0, 0, 0)}, B5 = {(1, 1, 0, 0, 0), (0, 1, 1, 0, 0)}
            p4 = C_Polyhedron(cs)
            p4.add_constraint(x >= L + 1)
            p4.add_constraint(z2 == 1)
            p4.add_constraint(L >= x + 1)
            p4.add_constraint(x1 == L  - x)
            p4.add_constraint(z1 == 0)                       
            print_generators(p4)
            print(f"contains integers: {p4.contains_integer_point()}")
            print("----------------------------")
            # A2 = {(1, 0, 0, 1, 0)}, B2 = {(0, 1, 1, 0, 0), (1, 0, 0, 0, 0)}
            print("p5") 
            p5 = C_Polyhedron(cs)
            p5.add_constraint(x <= L)
            p5.add_constraint(z2 == 0)
            p5.add_constraint(L <= x)
            p5.add_constraint(x1 >= 1)
            p5.add_constraint(z1 == 1)                       
            print_generators(p5)
            print(f"contains integers: {p5.contains_integer_point()}")
            print("----------------------------")
            print("p6")
            # A4 = {(1, 0, 1, 1, 1)}, B4 = {(0, 1, 1, 0, 0), (0, 0, 1, 0, 0)}
            # Generator: ray(0, 1, 1, 0, 0)
            # Generator: ray(0, 0, 1, 0, 0)
            # Generator: ray(1, 0, 0, 0, 0)
            # Generator: point(1/1, 0/1, 1/1, 1/1, 1/1)            
            p6 = C_Polyhedron(cs)
            p6.add_constraint(x >= L + 1)
            p6.add_constraint(z2 == 1)
            p6.add_constraint(L <= x)
            p6.add_constraint(x1 >= 1)
            p6.add_constraint(z1 == 1)                       
            print_generators(p6)
            print(f"contains integers: {p6.contains_integer_point()}")
            print("----------------------------")
            print("p7")
            # A2 = {(1, 0, 0, 1, 0)}, B2 = {(0, 1, 1, 0, 0), (1, 0, 0, 0, 0)}
            # Generator: ray(0, 1, 1, 0, 0)
            # Generator: point(1/1, 0/1, 0/1, 1/1, 0/1)
            # Generator: ray(1, 0, 0, 0, 0)
            # Generator: ray(1, 1, 0, 0, 0)
            p7 = C_Polyhedron(cs)
            p7.add_constraint(x <= L)
            p7.add_constraint(z2 == 0)
            p7.add_constraint(L >= x)
            p7.add_constraint(x1 >= L - x + 1)
            p7.add_constraint(z1 == 1)                       
            print_generators(p7)
            print(f"contains integers: {p7.contains_integer_point()}")

            print("----------------------------")   
            print("p8")        
            # Generator: ray(0, 1, 1, 0, 0)
            # Generator: ray(1, 1, 0, 0, 0)
            # Generator: ray(0, 1, 0, 0, 0)
            # Generator: point(0/1, 1/1, 0/1, 1/1, 0/1)
            p8 = C_Polyhedron(cs)
            p8.add_constraint(x <= L)
            p8.add_constraint(z2 == 0)
            p8.add_constraint(L >= x)
            p8.add_constraint(x1 <= L - x - 1)
            p8.add_constraint(z1 == 1)                       
            print_generators(p8)
            print(f"contains integers: {p8.contains_integer_point()}")
            print("----------------------------")
            print("p9")
            # Generator: ray(0, 1, 1, 0, 0)
            # Generator: ray(1, 1, 0, 0, 0)
            # Generator: ray(0, 1, 0, 0, 0)
            # Generator: point(0/1, 1/1, 0/1, 1/1, 0/1)
            p9 = C_Polyhedron(cs)
            p9.add_constraint(x >= L + 1)
            p9.add_constraint(z2 == 1)
            p9.add_constraint(L >= x + 1)
            p9.add_constraint(x1 >= L - x + 1)
            p9.add_constraint(z1 == 1)                       
            print_generators(p9)
            print(f"contains integers: {p9.contains_integer_point()}")

            print("----------------------------")
            print("p10")
            # Generator: ray(0, 1, 1, 0, 0)
            # Generator: ray(1, 1, 0, 0, 0)
            # Generator: ray(0, 1, 0, 0, 0)
            # Generator: point(0/1, 1/1, 0/1, 1/1, 0/1)
            p10 = C_Polyhedron(cs)
            p10.add_constraint(x >= L + 1)
            p10.add_constraint(z2 == 1)
            p10.add_constraint(L >= x + 1)
            p10.add_constraint(x1 <= L - x - 1)
            p10.add_constraint(z1 == 1)                       
            print_generators(p10)
            print(f"contains integers: {p10.contains_integer_point()}")
            


if __name__ == "__main__":
    unittest.main()
