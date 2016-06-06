package ch.epfl.lca.genopri.secure.parallel;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;
import util.Utils;
import ch.epfl.lca.genopri.secure.utils.Debugger;
import ch.epfl.lca.genopri.secure.utils.FileUtils;
import ch.epfl.lca.genopri.secure.MetaReader;
import circuits.arithmetic.IntegerLib;
import flexsc.CompEnv;
import flexsc.Party;
import gc.BadLabelException;
import graphsc.parallel.Gadget;
import graphsc.parallel.Machine;
import graphsc.parallel.SortGadget;

public class SecureParallel_EAF_Processor<T> extends Gadget<T>{

	private static final int EAF_preserved_bits = MetaReader.EAF_WIDTH - MetaReader.EAF_OFFSET + 7;
	
	/** The study */
	String studyName;
	
	/** Reference allele frequency file name */
	String refName;
	
	public SecureParallel_EAF_Processor(CompEnv<T> env, Machine machine) {
		super(env, machine);
	}
	
	private boolean[][][] getInput(int inputLength, int garblerId, int processors) throws IOException {
		System.out.println("inputLength: " + inputLength);
		
		String inputSpec = machine.getInput();
		HashMap<String, String> specMap = FileUtils.getMapfromFile(inputSpec);
		studyName = specMap.get("study");
		refName = specMap.get("ref_af");
		MetaReader mr = new MetaReader(new File(studyName + (env.getParty().equals(Party.Alice) ? ".alice" : ".bob")));
		RefAFReader rar = new RefAFReader(new File(refName));
		HashMap<String, String[]> varMap = rar.getVariantMap();
		
		int[] eafs = new int[inputLength];
		boolean[][][] c = new boolean[2][inputLength][];
		int i = -1;
		while(mr.advanceLine()){
			i++;
			if(!(i >= garblerId * inputLength && i < (garblerId + 1) * inputLength))
				continue;
			int tmp = i - (garblerId * inputLength);
			eafs[tmp] = mr.getEAF();
			c[0][tmp] = Utils.fromInt(eafs[tmp], MetaReader.EAF_WIDTH);
 			if(varMap.containsKey(mr.getMarker())){
 				String[] var = varMap.get(mr.getMarker());
 				if(var[1].equals(mr.getEffectAllele()) && var[2].equals(mr.getNonEffectAllele()))
 					c[1][tmp] = Utils.fromFixPoint(
 							Double.valueOf(var[3]), 
 							MetaReader.EAF_WIDTH, MetaReader.EAF_OFFSET);
 				else if(var[1].equals(mr.getNonEffectAllele()) && var[2].equals(mr.getEffectAllele()))
 					c[1][tmp] = Utils.fromFixPoint(
 							1 - Double.valueOf(var[3]), 
 							MetaReader.EAF_WIDTH, MetaReader.EAF_OFFSET);
 				else
 					c[1][tmp] = null;
 			}
 			else
 				c[1][tmp] = null;
		}
		mr.closeStudy();

		return c;
	}

	@Override
	public Object secureCompute() throws Exception {
		long s = System.nanoTime();
		
		int inputLength = machine.getInputLength() / machine.getTotalMachines();
		boolean[][][] data = getInput(inputLength, machine.getGarblerId(), machine.getTotalMachines());
		
		Debugger.debug(machine.getGarblerId(), env, "Preparing input from study file '"+ studyName + "'");
		
		T[][]	aliceEafTData = env.inputOfAlice(data[0]),
				bobEafTData = env.inputOfBob(data[0]);
		
		Debugger.debug(machine.getGarblerId(), env, "END preparing input from study file '"+ studyName + "'");
		
		IntegerLib<T> intLib = new  IntegerLib<T>(env);
		T[][] A_xor_B_EAF = env.newTArray(aliceEafTData.length, 0);
		T[][] refEAF = env.newTArray(aliceEafTData.length, 0);
		
		/*
		 * XOR the two shares
		 */
		Debugger.debug(machine.getGarblerId(), env, "XORing EAF");
		long timing = System.currentTimeMillis();
		for(int j = 0; j < A_xor_B_EAF.length; j++){
			A_xor_B_EAF[j] = intLib.xor(aliceEafTData[j], bobEafTData[j]);
			if(data[1][j] != null)
				refEAF[j] = env.inputOfAlice(data[1][j]);
			else
				refEAF[j] = intLib.xor(aliceEafTData[j], bobEafTData[j]);
		}
		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		
		/*
		 * Add differential privacy noise to study EAF
		 */
		Debugger.debug(machine.getGarblerId(), env, "Adding differential privacy noises");
		double sensitivity = 1.0 / 1000;
	    double epsilon = 0.1;
	    double delta = 0.05;
	    DifferentialPrivacy dp = new DifferentialPrivacy(sensitivity, epsilon, delta);
	    double[] noises = dp.genNoises(A_xor_B_EAF.length, "gaussian");
	    boolean[][] fpNoises = new boolean[noises.length][];
	    for(int j = 0; j < noises.length; j++)
	    	fpNoises[j] = Utils.fromFixPoint(noises[j], MetaReader.EAF_WIDTH, MetaReader.EAF_OFFSET);
	    T[][] aliceNoises = env.inputOfAlice(fpNoises),
	    		bobNoises = env.inputOfBob(fpNoises);
    	T[] zeroEAF = env.inputOfAlice(Utils.fromFixPoint(0, MetaReader.EAF_WIDTH, MetaReader.EAF_OFFSET)),
    			oneEAF = env.inputOfAlice(Utils.fromFixPoint(1.0, MetaReader.EAF_WIDTH, MetaReader.EAF_OFFSET));
    	
		for(int j = 0; j < A_xor_B_EAF.length; j++){
			A_xor_B_EAF[j] = intLib.add(A_xor_B_EAF[j], aliceNoises[j]);
			A_xor_B_EAF[j] = intLib.add(A_xor_B_EAF[j], bobNoises[j]);
			T leqSignal = intLib.leq(A_xor_B_EAF[j], zeroEAF),
					geqSignal = intLib.geq(A_xor_B_EAF[j], oneEAF);
			A_xor_B_EAF[j] = intLib.mux(A_xor_B_EAF[j], zeroEAF, leqSignal);
			A_xor_B_EAF[j] = intLib.mux(A_xor_B_EAF[j], oneEAF, geqSignal);
		}
		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		
		/*
		 * Preserve only a predefined number of bits (i.e., the precision) for the EAF values,
		 * and concatenate the truncated study EAF and reference EAF
		 */
		
		Debugger.debug(machine.getGarblerId(), env, "Truncating precision of EAF values");
		timing = System.currentTimeMillis();
		T[][] eafPairs = env.newTArray(refEAF.length, EAF_preserved_bits * 2);
		for(int j = 0; j < A_xor_B_EAF.length; j++){
			System.arraycopy(refEAF[j], MetaReader.EAF_WIDTH - EAF_preserved_bits, eafPairs[j], 0, EAF_preserved_bits);
			System.arraycopy(A_xor_B_EAF[j], MetaReader.EAF_WIDTH - EAF_preserved_bits, eafPairs[j], EAF_preserved_bits, EAF_preserved_bits);
		}
		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		
		/*
		 * Sort the EAF value pairs
		 */
		Debugger.debug(machine.getGarblerId(), env, "Sorting EAF value pairs");
		timing = System.currentTimeMillis();
		
		DataGraphNode<T>[] nodes = new DataGraphNode[eafPairs.length];
		for (int i = 0; i < nodes.length; i++) {
			nodes[i] = new DataGraphNode<T>(eafPairs[i], env);
		}
		
		new SortGadget<T>(env, machine)
		.setInputs(nodes, DataGraphNode.getDataComparator(env, eafPairs[0].length))
		.secureCompute();
		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		
		/*
		 * De-duplicate
		 */
		Debugger.debug(machine.getGarblerId(), env, "De-duplicating EAF value pairs");
		timing = System.currentTimeMillis();
		T[] prevPair = nodes[0].getData();
		T[] maxPair = intLib.ones(nodes[0].getDataLength());
		maxPair[nodes[0].getDataLength() - 1] = intLib.SIGNAL_ZERO;
		for(int j = 1; j < nodes.length; j++){
			T eqSignal = intLib.eq(prevPair, nodes[j].getData());
			nodes[j].setData(intLib.mux(nodes[j].getData(), maxPair, eqSignal));
			prevPair = intLib.mux(nodes[j].getData(), prevPair, eqSignal);
		}
		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		
		/*
		 * Move all duplicated items to the end
		 */
		Debugger.debug(machine.getGarblerId(), env, "Moving duplicated EAF value pairs to the end");
		timing = System.currentTimeMillis();
		new SortGadget<T>(env, machine)
		.setInputs(nodes, DataGraphNode.getDataComparator(env, eafPairs[0].length))
		.secureCompute();
		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");

		print(machine.getGarblerId(), env, nodes);
		
		long e = System.nanoTime();
		System.out.println((env.getParty().equals(Party.Alice) ? "Garbler " : "Evaluator ") 
				+ machine.getGarblerId() + ": P-Z runtime " + (e-s)/1e9 + "s");
		
		return null;
	}
	
	private void print(int garblerId,
			final CompEnv<T> env,
			DataGraphNode<T>[] nodes) throws IOException, BadLabelException {
		BufferedWriter bw = null;
		if (Party.Alice.equals(env.getParty())) {
			 bw = new BufferedWriter(new FileWriter("out/EAF_" + machine.getInputLength() + ".out." + garblerId));
		}
		for(int i = 0; i < nodes.length; i++){
			boolean[] plainEAFPair = env.outputToAlice(nodes[i].getData());
			boolean[] eaf1Bools = new boolean[MetaReader.EAF_WIDTH];
			Arrays.fill(eaf1Bools, false);
			System.arraycopy(plainEAFPair, 0, eaf1Bools, MetaReader.EAF_WIDTH - EAF_preserved_bits, EAF_preserved_bits);
			boolean[] eaf2Bools = new boolean[MetaReader.EAF_WIDTH];
			Arrays.fill(eaf2Bools, false);
			System.arraycopy(plainEAFPair, EAF_preserved_bits, eaf2Bools, MetaReader.EAF_WIDTH - EAF_preserved_bits, EAF_preserved_bits);
			Double eaf1 = Utils.toFixPoint(eaf1Bools, MetaReader.EAF_OFFSET);
			Double eaf2 = Utils.toFixPoint(eaf2Bools, MetaReader.EAF_OFFSET);
			if (Party.Alice.equals(env.party)) {
				bw.write(eaf1 + "\t\t" + eaf2 + "\n");
			}
		}
		env.channel.flush();
		if(bw != null){
			bw.flush();
			bw.close();
		}
	}
	
	private void printBooleans(boolean[] array){
		for (int i = array.length - 1; i >= 0; i--)
			System.out.print(array[i] ? '1' : '0');
		System.out.println();
	}
}
