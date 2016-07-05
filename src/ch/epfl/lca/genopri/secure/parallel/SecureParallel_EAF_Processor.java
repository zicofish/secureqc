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
import ch.epfl.lca.genopri.secure.utils.MemoryHeapMap;
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
	
	/** These variables are kept as class variables only for the convenience of analyzing their memory consumption. */
	public T[][]	aliceEafTData, bobEafTData, A_xor_B_EAF, refEAF, aliceNoises, bobNoises, eafPairs;
	public T[] zeroEAF, oneEAF, prevPair, maxPair;
	public boolean[][][] data;
	public IntegerLib<T> intLib;
	public DataGraphNode<T>[] nodes;
	public boolean[][] fpNoises;
	public double[] noises;
	
	public SecureParallel_EAF_Processor(CompEnv<T> env, Machine machine) {
		super(env, machine);
		String inputSpec = machine.getInput();
		HashMap<String, String> specMap = FileUtils.getMapfromFile(inputSpec);
		studyName = specMap.get("study");
		refName = specMap.get("ref_af");
	}
	
	/*
	 * Too slow and consume too much memory when I use HashMap for the reference variants
	 */
//	private boolean[][][] getInput(int inputLength, int garblerId, int processors) throws IOException {
//		System.out.println("inputLength: " + inputLength);
//		
//		MetaReader mr = new MetaReader(new File(studyName + (env.getParty().equals(Party.Alice) ? ".alice" : ".bob")));
//		RefAFReader rar = new RefAFReader(new File(refName));
//		HashMap<String, String[]> varMap = rar.getVariantMap();
//		
//		int[] eafs = new int[inputLength];
//		boolean[][][] c = new boolean[2][inputLength][];
//		int i = -1;
//		while(mr.advanceLine()){
//			i++;
//			if(!(i >= garblerId * inputLength && i < (garblerId + 1) * inputLength))
//				continue;
//			int tmp = i - (garblerId * inputLength);
//			eafs[tmp] = mr.getEAF();
//			c[0][tmp] = Utils.fromInt(eafs[tmp], MetaReader.EAF_WIDTH);
// 			if(varMap.containsKey(mr.getMarker())){
// 				String[] var = varMap.get(mr.getMarker());
// 				if(var[1].equals(mr.getEffectAllele()) && var[2].equals(mr.getNonEffectAllele()))
// 					c[1][tmp] = Utils.fromFixPoint(
// 							Double.valueOf(var[3]), 
// 							MetaReader.EAF_WIDTH, MetaReader.EAF_OFFSET);
// 				else if(var[1].equals(mr.getNonEffectAllele()) && var[2].equals(mr.getEffectAllele()))
// 					c[1][tmp] = Utils.fromFixPoint(
// 							1 - Double.valueOf(var[3]), 
// 							MetaReader.EAF_WIDTH, MetaReader.EAF_OFFSET);
// 				else
// 					c[1][tmp] = null;
// 			}
// 			else
// 				c[1][tmp] = null;
//		}
//		mr.closeStudy();
//
//		System.out.println("A_xor_B_EAF: " + MemoryUtil.deepMemoryUsageOf(varMap) / 1000000.0 + "Mbytes");
//		
//		return c;
//	}
	

	private boolean[][][] getInput(int inputLength, int garblerId, int processors) throws IOException {
		System.out.println("inputLength: " + inputLength);
		
		MetaReader mr = new MetaReader(new File(studyName + (env.getParty().equals(Party.Alice) ? ".alice" : ".bob")));
		RefAFReader rar = new RefAFReader(new File(refName));
		
		boolean[][][] c = new boolean[2][inputLength][];
		char refAllele, otherAllele, effectAllele, nonEffectAllele;
		double refAlleleFreq = -1;
		int i = -1;
		while(mr.advanceLine() && rar.advanceLine()){
			i++;
			if(i >= (garblerId + 1) * inputLength)
				break;
			if(i < garblerId * inputLength)
				continue;
			int tmp = i - (garblerId * inputLength);
			c[0][tmp] = Utils.fromInt(mr.getEAF(), MetaReader.EAF_WIDTH);
			refAllele = rar.getRefAllele();
			otherAllele = rar.getOtherAllele();
			effectAllele = mr.getEffectAllele();
			nonEffectAllele = mr.getNonEffectAllele();
			refAlleleFreq = rar.getRefAlleleFreq();
 			if(refAlleleFreq < 0)
 				c[1][tmp] = null;
 			else if(refAllele == effectAllele && otherAllele == nonEffectAllele)
				c[1][tmp] = Utils.fromFixPoint(
						refAlleleFreq, 
						MetaReader.EAF_WIDTH, MetaReader.EAF_OFFSET);
			else if(refAllele == nonEffectAllele && otherAllele == effectAllele)
				c[1][tmp] = Utils.fromFixPoint(
						1 - refAlleleFreq, 
						MetaReader.EAF_WIDTH, MetaReader.EAF_OFFSET);
			else
				c[1][tmp] = null;
		}
		mr.close();
		rar.close();
		
		return c;
	}
	
	@Override
	public Object secureCompute() throws Exception {
		Debugger.setLogFile("./log/" + (env.getParty().equals(Party.Alice) ? "Garbler_" : "Evaluator_") 
				+ machine.getGarblerId() + "_EAF.log");
		
		long s = System.nanoTime();
		/*
		 * Get input from file
		 */
		Debugger.debug(machine.getGarblerId(), env, "Getting input from study file '"+ studyName + "'");
		long timing = System.currentTimeMillis();
		
		int inputLength = machine.getInputLength() / machine.getTotalMachines();
		data = getInput(inputLength, machine.getGarblerId(), machine.getTotalMachines());
		
		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		
		/*
		 * Transform input into garble circuit signals
		 */
		
		Debugger.debug(machine.getGarblerId(), env, "Transforming input into garble circuit signals");
		timing = System.currentTimeMillis();
		
		aliceEafTData = env.inputOfAlice(data[0]);
		bobEafTData = env.inputOfBob(data[0]);
		
		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		
		intLib = new  IntegerLib<T>(env);
		A_xor_B_EAF = env.newTArray(aliceEafTData.length, 0);
		refEAF = env.newTArray(aliceEafTData.length, 0);
		
		/*
		 * XOR the two shares
		 */
		Debugger.debug(machine.getGarblerId(), env, "XORing EAF");
		timing = System.currentTimeMillis();
		for(int j = 0; j < A_xor_B_EAF.length; j++){
			A_xor_B_EAF[j] = intLib.xor(aliceEafTData[j], bobEafTData[j]);
			if(data[1][j] != null)
				refEAF[j] = env.inputOfAlice(data[1][j]);
			else
				refEAF[j] = intLib.xor(aliceEafTData[j], bobEafTData[j]);
		}
		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		data = null;
		aliceEafTData = null;
		bobEafTData = null;
		
		/*
		 * Add differential privacy noise to study EAF
		 */
		Debugger.debug(machine.getGarblerId(), env, "Adding differential privacy noises");
		timing = System.currentTimeMillis();
		double sensitivity = 1.0 / 1000;
	    double epsilon = 0.1;
	    double delta = 0.05;
	    DifferentialPrivacy dp = new DifferentialPrivacy(sensitivity, epsilon, delta);
	    noises = dp.genNoises(A_xor_B_EAF.length, "gaussian");
	    fpNoises = new boolean[noises.length][];
	    for(int j = 0; j < noises.length; j++)
	    	fpNoises[j] = Utils.fromFixPoint(noises[j], MetaReader.EAF_WIDTH, MetaReader.EAF_OFFSET);
	    aliceNoises = env.inputOfAlice(fpNoises);
		bobNoises = env.inputOfBob(fpNoises);
    	zeroEAF = env.inputOfAlice(Utils.fromFixPoint(0, MetaReader.EAF_WIDTH, MetaReader.EAF_OFFSET));
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
		aliceNoises = null;
		bobNoises = null;
		fpNoises = null;
		noises = null;
		dp = null;
		
		/*
		 * Preserve only a predefined number of bits (i.e., the precision) for the EAF values,
		 * and concatenate the truncated study EAF and reference EAF
		 */
		
		Debugger.debug(machine.getGarblerId(), env, "Truncating precision of EAF values");
		timing = System.currentTimeMillis();
		eafPairs = env.newTArray(refEAF.length, EAF_preserved_bits * 2);
		for(int j = 0; j < A_xor_B_EAF.length; j++){
			System.arraycopy(refEAF[j], MetaReader.EAF_WIDTH - EAF_preserved_bits, eafPairs[j], 0, EAF_preserved_bits);
			System.arraycopy(A_xor_B_EAF[j], MetaReader.EAF_WIDTH - EAF_preserved_bits, eafPairs[j], EAF_preserved_bits, EAF_preserved_bits);
		}
		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		A_xor_B_EAF = null;
		refEAF = null;
		
		/*
		 * Sort the EAF value pairs
		 */
		Debugger.debug(machine.getGarblerId(), env, "Sorting EAF value pairs");
		timing = System.currentTimeMillis();
		
		nodes = new DataGraphNode[eafPairs.length];
		for (int i = 0; i < nodes.length; i++) {
			nodes[i] = new DataGraphNode<T>(eafPairs[i], env);
		}
		eafPairs = null;
		
		new SortGadget<T>(env, machine)
		.setInputs(nodes, DataGraphNode.getDataComparator(env, EAF_preserved_bits * 2))
		.secureCompute();
		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		
		/*
		 * De-duplicate
		 */
		Debugger.debug(machine.getGarblerId(), env, "De-duplicating EAF value pairs");
		timing = System.currentTimeMillis();
		prevPair = nodes[0].getData();
		maxPair = intLib.ones(nodes[0].getDataLength());
		maxPair[nodes[0].getDataLength() - 1] = intLib.SIGNAL_ZERO;
		for(int j = 1; j < nodes.length; j++){
			T eqSignal = intLib.eq(prevPair, nodes[j].getData());
			nodes[j].setData(intLib.mux(nodes[j].getData(), maxPair, eqSignal));
			prevPair = intLib.mux(nodes[j].getData(), prevPair, eqSignal);
		}
		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		prevPair = null;
		maxPair = null;
		
		/*
		 * Move all duplicated items to the end
		 */
		Debugger.debug(machine.getGarblerId(), env, "Moving duplicated EAF value pairs to the end");
		timing = System.currentTimeMillis();
		new SortGadget<T>(env, machine)
		.setInputs(nodes, DataGraphNode.getDataComparator(env, EAF_preserved_bits * 2))
		.secureCompute();
		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");

		print(machine.getGarblerId(), env, nodes);
		nodes = null;
		
		long e = System.nanoTime();
		Debugger.debug(machine.getGarblerId(), env, "Total runtime: EAF runtime " + (e-s)/1e9 + "s");
		
		MemoryHeapMap.printGeneralMemInfo();
		
//		MemoryHeapMap.dump(this, new File((env.getParty().equals(Party.Alice) ? "Garbler_" : "Evaluator_") 
//				+ machine.getGarblerId() + "_memory_dump.txt" ));
		
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
