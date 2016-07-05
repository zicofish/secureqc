#!/bin/sh
user='root'
ips=('icsil1-sqc.epfl.ch')
roles=('both')
program="${1}"
qc_protocol='ch.epfl.lca.genopri.secure.parallel.SecureParallel_EAF_Processor'
run_size=262144
input_spec='./input_spec/study1.txt'
garbler_num=2

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
        for ((i=0; i<=`expr ${#ips[@]} - 1`; i++))
        do
            ssh $user@${ips[i]} 'bash -s'  <<SCRIPT
            mkdir -p secureqc/run/log/
            cd secureqc/run
            case "${roles[i]}" in
                "garbler")
                    (./runOneGarblers.py ${qc_protocol} ${run_size} ${garbler_num} ${input_spec} > foo.out 2> foo.err &)
                    ;;
                "evaluator")
                    (./runOneEvaluators.py ${qc_protocol} ${run_size} ${garbler_num} ${input_spec} > foo.out 2> foo.err &)
                    ;;
                "both")
                    (./runOneGarblers.py ${qc_protocol} ${run_size} ${garbler_num} ${input_spec} > foo.out 2> foo.err &)
                    (./runOneEvaluators.py ${qc_protocol} ${run_size} ${garbler_num} ${input_spec} > foo.out 2> foo.err &)
                    ;;
            esac
SCRIPT
        done
        ;;
esac
