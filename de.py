from scipy.optimize import differential_evolution, minimize
import numpy as np

def funx(x):
    return x**2 + 1

bounds = [(-5,5)]

result = differential_evolution(funx, bounds)
print(result)
print(result.x)
