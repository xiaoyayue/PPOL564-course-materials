import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt


# Define some transition matrix
T = np.array([[.2,.5],
              [.8,.5]])
rain = np.array([1,0])

v,e = la.eig(T)
v = np.diag(v)
e.dot(v**100).dot(la.inv(e)).dot(rain).round(2)


# Let's see how long it takes to reach a steady state
stay = []
for i in range(25):
    stay.append(e.dot(v**i).dot(la.inv(e)).dot(rain).round(2))
    
# Plot the outcom  
plt.figure()
plt.plot(stay)
plt.show()