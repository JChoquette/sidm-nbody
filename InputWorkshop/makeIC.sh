#!/bin/bash


for i in 0.01 0.02 0.05 0.1 0.2 0.5
do
	echo $i
	python 5050.py $i
done

