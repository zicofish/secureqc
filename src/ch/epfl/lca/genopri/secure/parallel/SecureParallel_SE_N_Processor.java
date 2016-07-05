package ch.epfl.lca.genopri.secure.parallel;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

import util.Utils;
import ch.epfl.lca.genopri.secure.MetaReader;
import ch.epfl.lca.genopri.secure.utils.Debugger;
import circuits.CircuitLib;
import flexsc.CompEnv;
import flexsc.Party;
import gc.BadLabelException;
import graphsc.parallel.Gadget;
import graphsc.parallel.Machine;
import graphsc.parallel.SortGadget;

public class SecureParallel_SE_N_Processor<T> extends Gadget<T>{	
	
	/** The study */
	String studyName;
	
	/** The maximum sample size of the study */
	Double Nmax;
	
	public SecureParallel_SE_N_Processor(CompEnv<T> env, Machine machine) {
		super(env, machine);
	}
	
	private boolean[][] getInput(int inputLength, int garblerId, int processors) throws IOException {
		System.out.println("inputLength: " + inputLength);
		
		studyName = machine.getInput();
		MetaReader mr = new MetaReader(new File(studyName + (env.getParty().equals(Party.Alice) ? ".alice" : ".bob")));
		
		int[] standardErrors = new int[inputLength];
		Nmax = 0.0;
		int i = -1;
		while(mr.advanceLine()){
			i++;
			Double tmpN = mr.getN();
			if(Nmax < tmpN) Nmax = tmpN;
			if(!(i >= garblerId * inputLength && i < (garblerId + 1) * inputLength))
				continue;
			standardErrors[i - (garblerId * inputLength)] = mr.getSE();
		}
		mr.close();
		
		boolean[][] c = new boolean[standardErrors.length][];
		for(i = 0; i < standardErrors.length; ++i) {
			c[i] = Utils.fromInt(standardErrors[i], MetaReader.SE_WIDTH);
		}
		return c;
	}

	@Override
	public Object secureCompute() throws Exception {
		Debugger.setLogFile("./log/" + (env.getParty().equals(Party.Alice) ? "Garbler_" : "Evaluator_") 
				+ machine.getGarblerId() + "_SE_N.log");
		
		long s = System.nanoTime();
		
		/*
		 * Get input from file
		 */
		Debugger.debug(machine.getGarblerId(), env, "Getting input from study file '"+ studyName + "'");
		long timing = System.currentTimeMillis();
		
		int inputLength = machine.getInputLength() / machine.getTotalMachines();
		boolean[][] data = getInput(inputLength, machine.getGarblerId(), machine.getTotalMachines());
		
		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		
		/*
		 * Transform input into garble circuit signals
		 */
		Debugger.debug(machine.getGarblerId(), env, "Transforming input into garble circuit signals");
		timing = System.currentTimeMillis();
		
		T[][] aliceTData, bobTData;
		aliceTData = (T[][]) env.inputOfAlice(data);
		bobTData = (T[][]) env.inputOfBob(data);
		
		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		
		/*
		 * XOR the two shares
		 */
		Debugger.debug(machine.getGarblerId(), env, "XORing standard error shares");
		timing = System.currentTimeMillis();
		
		CircuitLib<T> lib = new  CircuitLib<T>(env);
		T[][] A_xor_B = env.newTArray(data.length, MetaReader.SE_WIDTH);
		for(int j = 0; j < data.length; j++)
			A_xor_B[j] = lib.xor(aliceTData[j], bobTData[j]);
		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		aliceTData = bobTData = null;
		
		/*
		 * Sorting the standard erros
		 */
		Debugger.debug(machine.getGarblerId(), env, "Sorting standard errors");
		timing = System.currentTimeMillis();
		
		DataGraphNode<T>[] nodes = new DataGraphNode[data.length];
		for (int i = 0; i < nodes.length; i++) {
			nodes[i] = new DataGraphNode<T>(A_xor_B[i], env);
		}
		A_xor_B = null;
		
		new SortGadget<T>(env, machine)
		.setInputs(nodes, DataGraphNode.getDataComparator(env, MetaReader.SE_WIDTH))
		.secureCompute();
		
		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		
		print(machine.getGarblerId(), env, nodes);
		nodes = null;
		
		long e = System.nanoTime();
		Debugger.debug(machine.getGarblerId(), env, "Total runtime: SE-N runtime " + (e-s)/1e9 + "s");
		
		return null;
	}

	private void print(int garblerId,
			final CompEnv<T> env,
			DataGraphNode<T>[] nodes) throws IOException, BadLabelException {
		
		BufferedWriter bw = null;
		int medianIdx = machine.getInputLength() / 2, oneGarblerInputLength = machine.getInputLength() / machine.getTotalMachines();
		int garblerIdOfMedian = medianIdx / oneGarblerInputLength;
		int medianIdxInsideGarbler = medianIdx % oneGarblerInputLength;
		if (Party.Alice.equals(env.getParty())) {
			 bw = new BufferedWriter(new FileWriter("out/SE_N_" + machine.getInputLength() + ".out." + garblerId));
		}
		env.channel.flush();
		if(garblerId == garblerIdOfMedian){
				double median = Utils.toFixPoint(env.outputToAlice(nodes[medianIdxInsideGarbler].getData()), MetaReader.SE_OFFSET);
				if (Party.Alice.equals(env.party)) {
					bw.write(studyName + "\t" + Nmax + "\t" + median + "\n");
				}
		}
		if(bw != null){
			bw.flush();
			bw.close();
		}
	}

}
	