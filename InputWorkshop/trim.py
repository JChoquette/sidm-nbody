import numpy as np
from matplotlib import rc
import pylab as plt
import sys
import struct
import pygadgetreader as pg
import random

with open('cube1e12', mode='rb') as file:
	filecontent = file.read()
	file.close()

f=0
N=pg.readheader('cube1e12',"dmcount")
PPos=[]
PVel=[]
PID=[]
PMass=[]
for i in range(N):
	#Read Everything
	#The positions start at byte 268 (264-268 is an int 12*N)
	PPos.append(filecontent[268+12*i:268+12*i+12])
	#The velocities start at byte 276+12*N (8 previous bytes are 12*N, repeated twice)
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
	position=struct.unpack("fff",PPos[i])
	position=[p-1550.0 for p in position]
	if(pow(position[0],2)+pow(position[1],2)+pow(position[2],2)>pow(1550,2)):continue
	PPos2=PPos2+struct.pack('fff',position[0],position[1],position[2])
	PVel2=PVel2+PVel[i]
	PID2=PID2+struct.pack('i',i)


N=len(PPos2)/12
#packN=struct.pack('iiiiii',0,int(0.5*N),0,0,N-int(0.5*N),0)
packN=struct.pack('iiiiii',0,N,0,0,0,0)
M=struct.unpack("dddddd",filecontent[28:28+8*6])
print N
print M
#packM=struct.pack('dddddd',0,2*f*M[1],0,0,2*(1-f)*M[1],0)
packM=struct.pack('dddddd',0,M[1],0,0,0,0)
filecontentnew=filecontent[:4]+packN+packM+filecontent[76:100]+packN+filecontent[124:264]

print len(filecontentnew)

filecontentnew=filecontentnew+struct.pack("i",12*N)
filecontentnew=filecontentnew+PPos2
print len(PPos2)/12
filecontentnew=filecontentnew+struct.pack("i",12*N)
filecontentnew=filecontentnew+struct.pack("i",12*N)
filecontentnew=filecontentnew+PVel2
filecontentnew=filecontentnew+struct.pack("i",12*N)
filecontentnew=filecontentnew+struct.pack("i",4*N)
filecontentnew=filecontentnew+PID2
filecontentnew=filecontentnew+struct.pack("i",4*N)
#filecontentnew=filecontentnew+struct.pack("i",4*N)
#for i in range(N):filecontentnew=filecontentnew+struct.pack("f",M[1])
#filecontentnew=filecontentnew+struct.pack("i",4*N)

with open('cloud_trimmed', mode='wb') as file:
	file.write(filecontentnew)
	file.close()

#This just checks to make sure the file completed correctly
filename='cloud_trimmed'
print pg.readheader(filename,"dmcount")
print pg.readheader(filename,"time")
print pg.readheader(filename,"redshift")
print pg.readsnap(filename,"mass","dm")[0]
