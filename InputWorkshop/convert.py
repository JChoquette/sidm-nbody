import numpy as np
from matplotlib import rc
import pylab as plt
import sys
import struct
import pygadgetreader as pg
import random

with open('nfw_random', mode='rb') as file:
	filecontent = file.read()
	file.close()

#f is the SIDM fraction, Ndm is the total number of particles you want. This script randomly samples the input file, choosing f*Ndm particles to be SIDM and the remaining (f-1)*Ndm will be non-interacting (or rather will be of the second species). The reason for the random sampling is that I don't know how particles are distributed in the input file, there could be ordering (ex. lower radii are more likely at smaller array values)
f=0.1
Ndm=-1 #-1 for default (leave total number of particles unchanged). This removes the random sampling.

#This array lists the number of particles of each species
N=struct.unpack("iiiiii",filecontent[4:28])
print N

if(Ndm==-1):
	#This leaves the number of particles unchanged, and therefore we don't rely on the random sampling.
	Ndm=N[1]
	packN=struct.pack('iiiiii',0,int(Ndm*f),0,0,Ndm-int(Ndm*f),0)
	M=struct.unpack("dddddd",filecontent[28:28+8*6])
	print M
	packM=struct.pack('dddddd',0,M[1],0,0,M[1],0)
	filecontentnew=filecontent[:4]+packN+packM+filecontent[76:100]+packN+filecontent[124:]
else:
	#creates the new number array
	packN=struct.pack('iiiiii',0,int(Ndm*f),0,0,Ndm-int(Ndm*f),0)
	#recalibrate the masses (the total mass must remain the same, so the per particle mass must change)
	M=struct.unpack("dddddd",filecontent[28:28+8*6])
	print M
	packM=struct.pack('dddddd',0,N[1]/Ndm*M[1],0,0,N[1]/Ndm*M[1],0)
	#Now we have to cycle through, randomly choosing particles to add to the array
	PPos=''
	PVel=''
	PID=''
	PMass=''
	for i in range(Ndm):
		#pick a random particle
		n=random.randrange(N[1])
		#add it to the lists
		#A key point to note is that the format of the file differs a bit from what's in the documentation. Each block (Header, Pos, Vel, Id) is bracketed by a 4-byte integer before and after equal to the number of bytes in that block. So the header, for example, does not go from 0-256, but rather 4-260, with 0-4 and 260-264 both being the integer 256. I can't find mention of this in the documentation.
		#The positions start at byte 268 (264-268 is an int 12*N)
		PPos = PPos+filecontent[268+12*n:268+12*n+12]
		#The positions start at byte 276+12*N (8 previous bytes are 12*N, repeated twice)
		PVel = PVel+filecontent[276+12*N[1]+12*n:276+12*N[1]+12*n+12]
		#The particle IDs start at byte 284+24*N (8 previous bytes are 12*N then 4*N)
		PID = PID+filecontent[284+24*N[1]+4*n:284+24*N[1]+4*n+4]
		#This is followed by 4 bytes, 4*N. The particle mass array is not present in the file.
		#PMass = PMass+filecontent[280+28*N[1]+4*n:280+28*N[1]+4*n+4]


	#Create the new file, packing up and concatenating all the data
	filecontentnew=filecontent[:4]+packN+packM+filecontent[76:100]+packN+filecontent[124:264]+struct.pack('i',Ndm*12)+PPos+struct.pack('i',Ndm*12)+struct.pack('i',Ndm*12)+PVel+struct.pack('i',Ndm*12)+struct.pack('i',Ndm*4)+PID+struct.pack('i',Ndm*4)
	

with open('output', mode='wb') as file:
	file.write(filecontentnew)
	file.close()

#This just checks to make sure the file completed correctly
filename='output'
print pg.readheader(filename,"dmcount")
print pg.readheader(filename,"starcount")
print pg.readsnap(filename,"mass",'dm')[0]
