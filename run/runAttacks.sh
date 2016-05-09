#!/bin/bash

#numOfSNPs=(10 100 200)
#suffix=("dp0.01")
numOfSNPs=(1000 5000 10000 50000 100000 500000 1000000)
suffix=("" "dp1" "dp0.5" "dp0.1" "dp0.05" "dp0.01")

cd ../script/attacks
for ((i=0; i<=`expr ${#numOfSNPs[@]} - 1`; i++))
do
	for ((j=0; j<=`expr ${#suffix[@]} - 1`; j++))
	do
		python HomerAttack.py ${numOfSNPs[i]} ${suffix[j]} &
	done
done