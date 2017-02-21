from necpp import *
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# import user modules
import impedance
nl=100 # number of scanned points for length
nr=50 # number of scanned points for radius
lengths=np.linspace(0.2, 5.0, nl)
radii=np.linspace(0.002, 0.005, nr)
z0=50 # instrinsic impedance

reflections=np.zeros((nl,nr))

for i in range(nl):
  for j in range(nr):
    z = impedance.impedance(freq=134.5, base=0.5, length=lengths[i], radius=radii[j])
    reflections[i,j]=impedance.gamma(z,z0)


#plt.plot(lengths, reflections)
R, L = np.meshgrid(radii, lengths)
fig=plt.figure(figsize=(11,7),dpi=100)
ax=plt.subplot(111)
c=ax.contourf(L, R, reflections, cmap=cm.coolwarm)
plt.xlabel("Antenna length (m)")
plt.ylabel("Radius (m)")
plt.title("Reflection Coefficient vs Length and Radius")
cb=plt.colorbar(c)
plt.show()
