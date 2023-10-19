"""
This is an implementation of important benchmark cost functions.
For the formula of important bencahmark costs, you can visit the links below.
https://arxiv.org/pdf/1807.01844.pdf
https://arxiv.org/pdf/1809.09284.pdf
"""
import numpy as np
from typing import List

def schwefel(x: List[float]) -> float:
    d = len(x)
    f = 418.9829 * d
    for xi in x:
        f = f - (xi * np.sin(np.sqrt(np.abs(xi))))
    return f
