import numpy as np
from matplotlib import rc
import pylab as plt
import sys
import struct
import pygadgetreader as pg
import random


def getRad(array):
	return pow(pow(array[0],2)+pow(array[1],2)+pow(array[2],2),0.5)


filename="original_nfw"

nparts = pg.readheader(filename,"dmcount")
dmmass=pg.readsnap(filename,"mass",'dm')[0]

	
bins=[0+i/5.0 for i in range(20)]
	
pos=pg.readsnap(filename,"pos","dm")
vel=pg.readsnap(filename,"vel","dm")
	
radii=[]
vels=[]
for i in range(nparts):
	radii.append(getRad(pos[i]))
	vels.append(getRad(vel[i]))

M=[0.0 for i in range(len(bins))]
N=[0 for i in range(len(bins))]
vbar=[0.0 for i in range(len(bins))]
vdisp=[0.0 for i in range(len(bins))]
for j in range(len(radii)):
	for i in range(len(bins)):
		if radii[j]<pow(10,bins[i]):
			N[i]=N[i]+1
			vbar[i]=vbar[i]+vels[j]
			break
V=[]
rho=[]
for i in range(len(bins)):
	if(vbar[i]>0):vbar[i]=vbar[i]/N[i]
	M[i]=N[i]*dmmass
	v=4*3.14/3*pow(pow(10,bins[i]),3)
	if(i>0):v=v-4*3.14/3*pow(pow(10,bins[i-1]),3)
	V.append(v)
	rho.append(M[i]/V[i])
	if(i>0):M[i]=M[i]+M[i-1]

for j in range(len(radii)):
	for i in range(len(bins)):
		if radii[j]<pow(10,bins[i]):
			vdisp[i]=vdisp[i]+pow(vels[j]-vbar[i],2)
			break
for i in range(len(bins)):
	if(vdisp[i]>0):vdisp[i]=pow(vdisp[i]/N[i],0.5)

if(False):
	radarray=np.pow(10,bins)
	#Energy Conservation Stuff
	Mtck = interpolate.splrep(r,M,s=0)
	G=6.7E-11*1e10*2e30/31e18
	E=0
	for i in range(len(pos)):
		r=getRad(pos[i])
		v=getRad(vel[i])
		Mint=interpolate.splev(radarray,Mtck,der=0)
		U=-G*Mint/r
		K=0.5*v*v
		E=E+U+K
	print E
	

r=[pow(10.0,bins[i]) for i in range(len(bins))]
#y=[pow(vdisp[i],3)*pow(r[i],-1.875)/rho[i] for i in range(len(bins))]
y=vdisp
print vbar
plt.plot(bins,np.log10(y))
plt.show()

	

