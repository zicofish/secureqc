#!/usr/bin/python
import subprocess
import os.path
import time
import sys
inputLength = sys.argv[2]
garblers = sys.argv[3]
experiment = sys.argv[1]
input_spec = sys.argv[4]
subprocess.call("./clear_ports.sh", shell=True)
params = str(garblers) + " " + str(inputLength) + " " + experiment + " 00 REAL false " + input_spec
subprocess.call(["./run_garblers.sh " + params], shell=True)
