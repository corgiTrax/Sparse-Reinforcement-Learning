from scipy.optimize import differential_evolution, minimize
import numpy as np
import math

class de:
    def __init__(self):
        pass
    
    def funx(self, x):
        print("constrcuted")
        return x**3

    def solve(self):
        bounds = [(-5,5)]
        result = differential_evolution(self.funx, bounds)
        print(result)
        print(result.x)

new_de = de()
new_de.solve()

print(math.exp(3))


