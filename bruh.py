import re
import numpy as np
import sympy as sp
from scipy import integrate
import matplotlib.pyplot as plt

from asdf_core import asdf_Core
core = asdf_Core()

r = core.residual('1.27',0)

# Get all unique symbolic variables in the residual
vars_in_r = sorted(r.free_symbols, key=lambda s: s.name)

# Print their names
print([v.name for v in vars_in_r])
sp.pretty_print(r)


sol = sp.solve(sp.Eq(r, 0), sp.Symbol('p_{cns}'))
sp.pretty_print(sol)
