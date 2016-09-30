#!/bin/bash

#numOfSNPs=(10 100 200)
#suffix=("dp0.01")
#numOfSNPs=(1000 5000 10000 50000 100000 500000 1000000)
#suffix=("clear" "dp1" "dp0.5" "dp0.1" "dp0.05" "dp0.01")

#numOfSNPs=(10000 50000 100000 500000 1000000)
#suffix=("dp0.1_delta0.01" "dp0.1_delta0.05" "dp0.1_delta0.001" "dp0.1_delta0.005" "dp0.05_delta0.01" "dp0.05_delta0.001" "dp0.05_delta0.05" "dp0.05_delta0.005")

cd ../script/attacks
for ((i=0; i<=`expr ${#numOfSNPs[@]} - 1`; i++))
do
	for ((j=0; j<=`expr ${#suffix[@]} - 1`; j++))
	do
		(python HomerAttack.py ${numOfSNPs[i]} ${suffix[j]} &)
	done
done

# pairwise
numpOfSNPs=(752 829 10024 11084 108856 119132 687 769 9128 10355 99617 112151 1008 1067 14095 15282 150914 164068 923 1037 12840 14535 137365 155331)
suffix=("dp0.1_delta0.01" "dp0.1_delta0.001" "dp0.1_delta0.01" "dp0.1_delta0.001" "dp0.1_delta0.01" "dp0.1_delta0.001" "dp0.1_delta0.05" "dp0.1_delta0.005" "dp0.1_delta0.05" "dp0.1_delta0.005" "dp0.1_delta0.05" "dp0.1_delta0.005" "dp0.05_delta0.01" "dp0.05_delta0.001" "dp0.05_delta0.01" "dp0.05_delta0.001" "dp0.05_delta0.01" "dp0.05_delta0.001" "dp0.05_delta0.05" "dp0.05_delta0.005" "dp0.05_delta0.05" "dp0.05_delta0.005" "dp0.05_delta0.05" "dp0.05_delta0.005")

cd ../script/attacks
for ((i=0; i<=`expr ${#numOfSNPs[@]} - 1`; i++))
do
	(python HomerAttack.py ${numOfSNPs[i]} ${suffix[i]} &)
done