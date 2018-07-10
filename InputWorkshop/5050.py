import numpy as np
from matplotlib import rc
import pylab as plt
import sys
import struct
import pygadgetreader as pg
import random

#infile='smoothbump_MED'
#outfile='ICDIR/smoothbump_'+str(int(float(sys.argv[1])*100))+'_MED'
infile='100kparticles'
outfile='nfw_small'

with open(infile, mode='rb') as file:
	filecontent = file.read()
	file.close()

#f is the SIDM fraction, Ndm is the total number of particles you want. This script takes the random NFW profile (as input) and makes half the dark matter particles non-interacting. It then adjusts the masses so as to give the desired SIDM fraction (by mass).
f=float(sys.argv[1])
Ndm=-1 #-1 for default (leave total number of particles unchanged). This removes the random sampling.

#This array lists the number of particles of each species
N=struct.unpack("iiiiii",filecontent[4:28])
print N

if(Ndm==-1):
	#This leaves the number of particles unchanged, and therefore we don't rely on the random sampling.
	Ndm=N[1]
	packN=struct.pack('iiiiii',0,int(Ndm*0.5),0,0,Ndm-int(Ndm*0.5),0)
	M=struct.unpack("dddddd",filecontent[28:28+8*6])
	print M
	packM=struct.pack('dddddd',0,2*f*M[1],0,0,2*(1-f)*M[1],0)
	filecontentnew=filecontent[:4]+packN+packM+filecontent[76:100]+packN+filecontent[124:]
with open(outfile, mode='wb') as file:
	file.write(filecontentnew)
	file.close()

#This just checks to make sure the file completed correctly
print pg.readheader(outfile,"dmcount")
print pg.readheader(outfile,"starcount")
print pg.readsnap(outfile,"mass",'dm')[0]
