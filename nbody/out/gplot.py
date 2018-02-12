import numpy as np
from matplotlib import rc
import pylab as plt
import sys
import struct
import pygadgetreader as pg
import random


def getRad(array):
	return pow(pow(array[0],2)+pow(array[1],2)+pow(array[2],2),0.5)

#To run:
#Just do "python plot.py N"
#where N is the number of snapshots

N=int(sys.argv[1]) #Number of snps taken
Nskip=int(sys.argv[2])

from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.gca(projection='3d')
cm=plt.get_cmap('brg_r')
tspace=pg.readheader("snp_001","time")

for snp in range(0,N+1,Nskip):
	pg.readsnap
	print snp
	filename="snp_{:0>3d}".format(snp)
	fileContent=0
	nparts = pg.readheader(filename,"dmcount")+pg.readheader(filename,"starcount")
	dmmass=pg.readsnap(filename,"mass",'dm')[0]
	types = ['dm']
	if pg.readheader(filename,"starcount")>0: types.append('stars')

	
	bins=[0+i/5.0 for i in range(20)]
	M=[0.0 for i in range(len(bins))]
	
	for t in types:
		pos=pg.readsnap(filename,"pos",t)
		radii=[]
		for i in range(len(pos)):
			radii.append(getRad(pos[i]))
		for r in radii:
			for i in range(len(bins)):
				if r<pow(10,bins[i]):
					M[i]=M[i]+dmmass*len(pos)/nparts


	V=[]
	for i in range(len(bins)):
		v=4*3.14/3*pow(10,bins[i])
		if(i>0):v=v-4*3.14/3*pow(10,bins[i-1])
		V.append(v)
	rho=[np.log10(M[0]/V[0])]
	for i in range(1,len(bins)):
		rho.append(np.log10((M[i]-M[i-1])/V[i]))

	time = pg.readheader(filename,"time")
	ax.plot([time for i in range(len(bins))],bins,np.log10(M),c=cm(float(time)/float(N*tspace)))



plt.show()

