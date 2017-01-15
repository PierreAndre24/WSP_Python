import matplotlib.pyplot as plt
import numpy as np

x = np.array([1,2,3,4,5])
y = np.array([[1,2,3,4,5],[2,3,4,5,6]])
y = np.transpose(y)
# y = np.array([1,2,3,4,5])
plt.figure()
plt.plot(x,y)
plt.show()
