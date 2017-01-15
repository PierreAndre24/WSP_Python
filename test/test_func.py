import numpy as np
from libs.array_operations import *

ar = np.random.rand(3,3,3)

print ar
#print take_subarray(ar, [[1,3],[0]])
print n_transpose(ar, (1,0,2))
