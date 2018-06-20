import numpy as np
from matplotlib import rc
import pylab as plt
import sys
import struct
import pygadgetreader as pg
import random

infile = 'icsM10_random'
outfile = 'justbump'
with open(infile, mode='rb') as file:
	filecontent = file.read()
	file.close()

f=0
rbump=372.448
N=pg.readheader(infile,"dmcount")
M=struct.unpack("dddddd",filecontent[28:28+8*6])[1]
PPos=[]
PVel=[]
PID=[]
PMass=[]
for i in range(N):
	#Read Everything
	#The positions start at byte 268 (264-268 is an int 12*N)
	position=struct.unpack("fff",filecontent[268+12*i:268+12*i+12])
	PPos.append([p-1000.0 for p in position])
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
positions=[]
	
for i in range(len(PPos)):
	position=PPos[i]
	while(pow(position[0],2)+pow(position[1],2)+pow(position[2],2)>pow(rbump,2)):
		position[0]=random.uniform(-rbump,rbump)
		position[1]=random.uniform(-rbump,rbump)
		position[2]=random.uniform(-rbump,rbump)
	#PPos[i]=position
for i in range(len(PPos)):
	PPos2=PPos2+struct.pack('fff',PPos[i][0]+1000,PPos[i][1]+1000,PPos[i][2]+1000)
	PVel2=PVel2+struct.pack('fff',0.0,0.0,0.0)
	PID2=PID2+struct.pack('i',i)


N=len(PPos2)/12
#packN=struct.pack('iiiiii',0,int(0.5*N),0,0,N-int(0.5*N),0)
packN=struct.pack('iiiiii',0,N,0,0,0,0)
print N
print M
filecontentnew=filecontent[:264]

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

with open(outfile, mode='wb') as file:
	file.write(filecontentnew)
	file.close()

#This just checks to make sure the file completed correctly
filename=outfile
print pg.readheader(filename,"dmcount")
print pg.readheader(filename,"time")
print pg.readheader(filename,"redshift")
print pg.readsnap(filename,"mass","dm")[0]
