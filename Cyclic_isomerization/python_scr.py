#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 21:57:06 2021

@author: akhil
"""

import numpy as np
from io import StringIO
import subprocess
import sys
import time
import os
import os
import shutil

ofolder= os.getcwd()
ofolder = ofolder + '/'
mdname = 'M10D1A1_C25'
lammpscmd = '/usr/lib64/openmpi/bin/mpirun -np 8 --hostfile my_hosts /home/Akhil_CRSM/Installations/lammps/src/lmp_mpi -in lammps2.in >> log/terminal.log'
#subprocess.call(lammpscmd, shell=True)

Ndihedline = 35981
Ndiheds = 17334
Nlines = Ndihedline + Ndiheds + 2
TNlines = 62019

Tstep = 200000.0 #fs
Totaltime = 800 #ps

Ncycles = int(Totaltime*1000.0/Tstep) + 1

A = np.zeros([Ndiheds,6])

foldername = ofolder + 'Cycles/Dummy'
if os.path.isdir(foldername):
	shutil.rmtree(foldername,ignore_errors=True)
os.mkdir(foldername)

for Cycle_num in range(1,Ncycles):
	foldername = ofolder + 'Cycles/Cycle_' + str(Cycle_num) 
	if os.path.isdir(foldername):
		shutil.rmtree(foldername,ignore_errors=True)
	os.mkdir(foldername)

	os.chdir(foldername)

	srcdata = ofolder + 'Cycles/Cycle_' + str(Cycle_num-1) + '/' + mdname + '_tt' + str(1) + '.data'
	dstdata = ofolder + 'Cycles/Cycle_' + str(Cycle_num) + '/' + mdname + '_t' + str(0) + '.data'
	shutil.copy2(srcdata,dstdata)
	
	os.remove(srcdata)
		
	srcdata = ofolder + 'Cycles/Cycle_' + str(Cycle_num-1) + '/' + 'lammps2.in'
	dstdata = ofolder + 'Cycles/Cycle_' + str(Cycle_num) + '/' + 'lammps2.in'
	shutil.copy2(srcdata,dstdata)	
	
	srcdata = ofolder + 'Cycles/Cycle_' + str(Cycle_num-1) + '/' + 'my_hosts'
	dstdata = ofolder + 'Cycles/Cycle_' + str(Cycle_num) + '/' + 'my_hosts'
	shutil.copy2(srcdata,dstdata)	
	
	foldernamel = foldername + '/log' 
	os.mkdir(foldernamel)

	foldernamed = foldername + '/dump' 
	os.mkdir(foldernamed)
	
	subprocess.call(lammpscmd, shell=True)

	foldername = ofolder + 'Cycles/Dummy'
	if os.path.isdir(foldername):
		shutil.rmtree(foldername,ignore_errors=True)
	os.mkdir(foldername)	
	
	srcdata = ofolder + 'Cycles/Cycle_' + str(Cycle_num) + '/' + mdname + '_t' + str(1) + '.data'
	dstdata = ofolder + 'Cycles/Dummy/' + mdname + '_ta' + str(Cycle_num) + '.data'
	shutil.copy2(srcdata,dstdata)
	
	os.remove(srcdata)
	
	dstdatar = ofolder + 'Cycles/Dummy/' + mdname + '_ta' + str(Cycle_num) + '.data'
	dstdataw = ofolder + 'Cycles/Dummy/' + mdname + '_tb' + str(Cycle_num) + '.data'
	datafile = open(dstdatar,'r')
	datawfile = open(dstdataw,'w')

	count = 0
	count_trans = 0
	count_cis = 0
	for i in range(0,TNlines):
		count = count + 1
		line = datafile.readline()
		if ((count > Ndihedline + 1)and(count<Nlines)):
			# print(line)
			line1 = line.split(' ')
			# print(line1)
			if (int(line1[1])==81):
				# print(line)
				# print(line1)
				line1[1] = str(108)
				# print(line1)
				count_trans = count_trans + 1
			elif (int(line1[1])==108):
				# print(line)
				# print(line1)
				line1[1] = str(81)
				# print(line1)
				count_cis = count_cis + 1
			line = ''
			for j in range(0,5):
				line = line + line1[j] + ' '
			line = line + line1[5]
			# print(line) 
			datawfile.write(line)
		else:
			datawfile.write(line)
			

	datafile.close()
	datawfile.close()

	print('Cis-Trans', count_trans, 'Trans-Cis', count_cis)

	srcdata = ofolder + 'Cycles/Dummy/' + mdname + '_tb' + str(Cycle_num) + '.data'
	dstdata = ofolder + 'Cycles/Cycle_' + str(Cycle_num) + '/' + mdname + '_tt' + str(1) + '.data'	
	shutil.copy2(srcdata,dstdata)	
	#below two lines are not needed in the actual code as the file will be generated by lammps
	#dstdata = ofolder + 'Cycle_' + str(Cycle_num) + '/' + mdname + '_t' + str(1) + '.data'
	#shutil.copy2(srcdata,dstdata)
	
	os.chdir(ofolder)
	print('Cycle Number =',Cycle_num)