import numpy as np
import matplotlib.pyplot as plt

from rng import RNG
from nistrng import *


if __name__ == "__main__":
    """Plot histogram for RNG"""
    N = 100000
    bin_count = 100

    # Create pseudo-random array
    with RNG(456) as r:
        rand_array = np.array([r.get() for i in range(N)])

    # plot histogram - should be uniformly distributed
    frq, edges = np.histogram(rand_array, bin_count)
    fig, ax = plt.subplots()
    ax.bar(edges[:-1], frq, width=np.diff(edges), edgecolor="black", align="edge")
    plt.show()
