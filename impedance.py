from necpp import *
import math
import numpy as np

# define contants
sigma=1.45e6		# conductivity of stainless steel
ground_sigma=0.002  	# conductivity of ground
ground_eps=10 		# relative dielectric constant of ground
# handle returned error
def handle_err(status):
  if (status !=0):
    print(nec_error_message())

# set up geometry and condition for simulation
def geometry(freq, base, length, radius):
  wavelength=3e8/(1e6*freq)  	# freq unit is MHz
  n_seg=int(math.ceil(50*length/wavelength))
  nec=nec_create()   		# create nec object
  handle_err(nec_wire(nec, 1, n_seg, 0, 0, base, 0, 0, base+length, radius, 1.0, 1.0))  # create a monopole antenna
  handle_err(nec_geometry_complete(nec, 1))    # indicate the geometry is complete
  handle_err(nec_ld_card(nec, 5, 0, 0, 0, sigma, 0.0, 0.0))
  handle_err(nec_gn_card(nec, 0, 0, ground_eps, ground_sigma, 0, 0, 0, 0))
  handle_err(nec_fr_card(nec, 0, 1, freq, 0))  # freq unit is MHz
  handle_err(nec_ex_card(nec, 0, 0, int(n_seg/3), 0, 1.0, 0, 0, 0, 0, 0))
  return nec  # return nec geometry
  
# impedance calculation / antenna simulation
def impedance(freq, base, length, radius):
  nec=geometry(freq, base, length, radius)
  handle_err(nec_xq_card(nec, 0))   # execute the simulation in normal mode
  z = complex(nec_impedance_real(nec, 0), nec_impedance_imag(nec, 0))
  nec_delete(nec)
  return z

# compute the reflection coefficient based on z and z0
def gamma(z, z0):
  return np.abs((z-z0)/(z+z0))

if __name__=="__main__":
  z=impedance(freq=134.5, base=0.5, length=4.0, radius=0.002)
  relfect=gamma(z, z0=50)
  print(z.real, ";", z.imag)
  print(z)
  print(reflect)
