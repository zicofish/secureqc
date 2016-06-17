#!/bin/bash
javac -d bin -sourcepath ./src/ -cp `find ./lib/ -name "*.jar" | tr "\n" ":"` ./src/ch/epfl/lca/genopri/secure/parallel/SecureParallel_EAF_Processor.java