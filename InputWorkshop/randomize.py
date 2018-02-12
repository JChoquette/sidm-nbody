import numpy as np
from matplotlib import rc
import pylab as plt
import sys
import struct
import pygadgetreader as pg
import random

with open('original_nfw', mode='rb') as file:
	filecontent = file.read()
	file.close()

N=pg.readheader('original_nfw',"dmcount")
head=filecontent[0:268]
PPos=[]
PVel=[]
PID=[]
PMass=[]
for i in range(N):
	#Read Everything
	#The positions start at byte 268 (264-268 is an int 12*N)
	PPos.append(filecontent[268+12*i:268+12*i+12])
	#The positions start at byte 276+12*N (8 previous bytes are 12*N, repeated twice)
	PVel.append(filecontent[276+12*N+12*i:276+12*N+12*i+12])
	#The particle IDs start at byte 284+24*N (8 previous bytes are 12*N then 4*N)
	PID.append(filecontent[284+24*N+4*i:284+24*N+4*i+4])
	#This is followed by 4 bytes, 4*N. The particle mass array is not present in the file.
	#PMass.append(filecontent[280+28*N+4*i:280+28*N+4*i+4])


PPos2=''
PVel2=''
PID2=''
PMass2=''
for i in range(N):
	print i
	n=random.randrange(len(PPos))
	PPos2=PPos2+PPos[n]
	del(PPos[n])
	PVel2=PVel2+PVel[n]
	del(PVel[n])
	PID2=PID2+PID[n]
	del(PID[n])
	



#Create the new file, packing up and concatenating all the data
filecontentnew=head+PPos2+filecontent[268+12*N:268+12*N+8]+PVel2+filecontent[276+24*N:276+24*N+8]+PID2+filecontent[284+28*N:284+28*N+4]
	

with open('nfw_random', mode='wb') as file:
	file.write(filecontentnew)
	file.close()

#This just checks to make sure the file completed correctly
filename='nfw_random'
print pg.readheader(filename,"dmcount")
print pg.readsnap(filename,"mass",'dm')[0]
