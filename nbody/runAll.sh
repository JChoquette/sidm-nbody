#!/bin/bash

IFS=$'\n' read -d '' -r -a lines < ./runParams.txt

for i in {0..29}
do
	IFS=" "
	cols=(${lines[i]})
	cat ./dummyparams.txt | sed -e "s,INITCOND,${cols[0]},g" | sed -e "s,SIDMCROSSSECTION,${cols[1]},g" | tee ./tempparams.txt
	#mpiexec -n 32 ./sidm-gadget tempparams.txt
done
