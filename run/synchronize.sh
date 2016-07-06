#!/bin/bash
user='root'
ips=(10.156.12.1 10.156.12.2 10.156.12.3 10.156.12.4 10.156.12.5 10.156.12.7 10.156.12.8 10.156.12.9 10.156.12.10 10.156.12.11 10.156.12.12 10.156.12.13 10.156.12.14 10.156.12.15 10.156.12.16 10.156.12.17)
garblers=(8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0)
evaluators=(0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8)
program="${1}"
qc_protocol='ch.epfl.lca.genopri.secure.parallel.SecureParallel_EAF_Processor'
run_size=262144
input_spec='./input_spec/study1.txt'
garbler_num=64
jvm_mem='1536m'

case ${program} in
    "init_git")
        # Initialize the git repo on each machine
        read -s -p "Git password: " git_password
        for ((i=0; i<=`expr ${#ips[@]} - 1`; i++))
        do
	        ssh $user@${ips[i]} 'bash -s' <<SCRIPT
		    git clone https://zhihuang:${git_password}@git.epfl.ch/repo/secureqc.git
SCRIPT
        done
        ;;
    "sync_git")
        # Update git repo
        read -s -p "Git password: " git_password
        for ((i=0; i<=`expr ${#ips[@]} - 1`; i++))
        do
            ssh $user@${ips[i]} 'bash -s' <<SCRIPT
            cd secureqc
            git pull https://zhihuang:${git_password}@git.epfl.ch/repo/secureqc.git
SCRIPT
        done
        ;;
    "copy_data")
        # Copy data to each machine
        for ((i=0; i<=`expr ${#ips[@]} - 1`; i++))
        do
            ssh $user@${ips[i]} 'bash -s' <<SCRIPT
            cd secureqc
            mkdir -p data/reference/
            mkdir -p data/zk_jfellay/GIANT_toy/
SCRIPT
	        scp ../data/reference/aligned_AlleleFreq_HapMap_CEU_phase3.2_nr.b36_fwd.txt $user@${ips[i]}:~/secureqc/data/reference/
            scp ../data/zk_jfellay/GIANT_toy/CLEAN.AGES.HEIGHT.MEN.GT50.20100914.txt.alice ../data/zk_jfellay/GIANT_toy/CLEAN.AGES.HEIGHT.MEN.GT50.20100914.txt.bob $user@${ips[i]}:~/secureqc/data/zk_jfellay/GIANT_toy/
        done
        ;;
    "compile")
        # Compile the java code
        for ((i=0; i<=`expr ${#ips[@]} - 1`; i++))
        do
            ssh $user@${ips[i]} 'bash -s' <<SCRIPT
            cd secureqc
            mkdir -p bin
            javac -d bin -sourcepath ./src/ -cp \`find ./lib/ -name "*.jar" | tr "\\n" ":"\` ./src/ch/epfl/lca/genopri/secure/parallel/*.java
SCRIPT
        done
        ;;
    "run_gc")
        # Run the garble circuit
        garblerCounter=0
        evaluatorCounter=0
        for ((i=0; i<=`expr ${#ips[@]} - 1`; i++))
        do
            ssh $user@${ips[i]} 'bash -s'  <<SCRIPT
            mkdir -p secureqc/run/log/
            cd secureqc/run
            eval \$(ps awux | grep 'java .*parallel' | grep -v 'grep' | awk '{print "kill -9 " $2}')
            for ((j=0; j<${garblers[i]}; j++))
            do
                garblerID=\$(($garblerCounter + \$j))
                (java -Xmx${jvm_mem} -javaagent:../lib/classmexer.jar -cp ../bin/:../lib/*:../lib/commons-math3-3.6/* graphsc.parallel.Machine -garblerId \$garblerID  -garblerPort \$((35000 + \$garblerID)) -isGen true -inputLength ${run_size} -program ${qc_protocol} -totalGarblers ${garbler_num} -machineConfigFile 00 -mode REAL -peerBasePort 50000 -offline false -input ${input_spec} > foo.out 2> foo.err &)
            done
            
            for ((j=0; j<${evaluators[i]}; j++))
            do
                evaluatorID=\$(($evaluatorCounter + \$j))
                (java -Xmx${jvm_mem} -javaagent:../lib/classmexer.jar -cp ../bin/:../lib/*:../lib/commons-math3-3.6/* graphsc.parallel.Machine -garblerId \$evaluatorID  -garblerPort \$((35000 + \$garblerID)) -isGen false -inputLength ${run_size} -program ${qc_protocol} -totalGarblers ${garbler_num} -machineConfigFile 00 -mode REAL -peerBasePort 55000 -offline false -input ${input_spec} > foo.out 2> foo.err &)
            done            
SCRIPT
            garblerCounter=$(($garblerCounter + ${garblers[i]}))
            evaluatorCpunter=$(($evaluatorCounter + ${evaluators[i]}))
        done
        ;;
esac
