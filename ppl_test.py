from ppl import Variable, Constraint_System, C_Polyhedron,NNC_Polyhedron

import unittest


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

        print("Polyhedron:", ph)

        # Inspect generators (vertices and rays)
        gens = ph.minimized_generators()
        for g in gens:
            print("Generator:", g)


    def test_f2(self): 
        cs.insert(5*x + 2*y >= 17)
        cs.insert(3*x - y <= 8)
        cs.insert(2*x + 3*y <= 20)

        # Create polyhedron
        ph = NNC_Polyhedron(cs)

        print("Polyhedron:", ph)

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
        cs.insert(2*x >= 1)
        cs.insert(2 *y >= 1)
          
        # cs.insert(2 * x <= 1)  
        # cs.insert(2 * y <= 1)        

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




if __name__ == "__main__":
    unittest.main()
