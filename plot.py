from necpp import *
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import gridspec

# import user modules
import impedance

def compute(nl,nr,lengths,radii,z0):
	reflections=np.zeros((nr,nl))
	global prog  # show the computation progress
	prog=0 
	sig=0
	for i in range(nr):   # row for y axis
	  for j in range(nl):  # column for x axis
	    z = impedance.impedance(freq=134.5, base=0.5, length=lengths[j], radius=radii[i])
	    reflections[i,j]=impedance.gamma(z,z0)
	    sig+=1
	    prog=100*sig/(nl*nr)
	    print(prog)
	return reflections

def plot(lengths, radii, reflections):
	#plt.plot(lengths, reflections)
	L, R = np.meshgrid(lengths, radii)
	fig1=plt.figure(figsize=(10,4),dpi=100)
	fig1.suptitle("Reflection Coefficient vs Length and Radius")
	# set up the grid using gridspec
	gs=gridspec.GridSpec(1, 2, width_ratios=[1,1.2])		
	ax1=fig1.add_subplot(gs[0])
	#c1=ax1.contourf(L, R, reflections, cmap=cm.jet)
	c1=ax1.imshow(reflections, origin="lower", interpolation="bilinear", extent=[np.amin(lengths),np.amax(lengths),np.amin(radii),np.amax(radii)], cmap=cm.jet, aspect=(np.amax(lengths)-np.amin(lengths))/(np.amax(radii)-np.amin(radii)) )
	# shift position of 1st colobar	
	box1=ax1.get_position()
	axcb1=plt.axes([box1.x0*1.02 + box1.width * 1.02, box1.y0, 0.01, box1.height])
	cb1=plt.colorbar(c1, cax=axcb1)	
	ax1.set_xlabel("Antenna length (m)")
	ax1.set_ylabel("Radius (m)")
	#ax1.set_title("2D")
	ax2=fig1.add_subplot(gs[1],projection="3d")
	ax2.view_init(50,130)
	s2=ax2.plot_surface(L, R, reflections, cmap=cm.jet)
	# shift position of 2nd colobar
	box2=ax2.get_position()
	axcb2=plt.axes([box2.x0*1.05 + box2.width * 1.05, box2.y0, 0.01, box2.height])
	cb2=plt.colorbar(c1, cax=axcb2)
	ax2.set_xlabel("Antenna length (m)")
	ax2.set_ylabel("Radius (m)")
	ax2.set_zlabel("Reflection Coefficient")
	#ax2.set_title("3D")
	return fig1, ax1, ax2, cb1, cb2, axcb1, axcb2
	
if __name__=="__main__":
	reflections=compute(nl,nr,lengths,radii,z0)
	plot(lengths,radii,reflections)
	plt.show()
