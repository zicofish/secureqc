package ch.epfl.lca.genopri.secure.parallel;

import flexsc.CompEnv;
import flexsc.Party;
import gc.BadLabelException;
import graphsc.parallel.Gadget;
import graphsc.parallel.Machine;
import graphsc.parallel.SortGadget;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;

import org.apache.commons.math3.distribution.NormalDistribution;

import util.Utils;
import ch.epfl.lca.genopri.secure.MetaReader;
import ch.epfl.lca.genopri.secure.utils.Debugger;
import ch.epfl.lca.genopri.secure.utils.FileUtils;
import ch.epfl.lca.genopri.secure.utils.MemoryHeapMap;
import circuits.BitonicSortLib;
import circuits.arithmetic.FixedPointLib;
import circuits.arithmetic.IntegerLib;

public class SecureParallel_P_Z_Processor<T> extends Gadget<T>{
	
	private static final int P_preserved_bits = 7;
	
	private static final int Z_preserved_bits = 7;
	
	/** The study */
	String studyName;
	
	public SecureParallel_P_Z_Processor(CompEnv<T> env, Machine machine) {
		super(env, machine);
		String inputSpec = machine.getInput();
		HashMap<String, String> specMap = FileUtils.getMapfromFile(inputSpec);
		studyName = specMap.get("study");
	}
	
	private boolean[][][] getInput(int inputLength, int garblerId, int processors) throws IOException {
		System.out.println("inputLength: " + inputLength);

		MetaReader mr = new MetaReader(new File(studyName + (env.getParty().equals(Party.Alice) ? ".alice" : ".bob")));
		
		int[] betas = new int[inputLength], ses = new int[inputLength];
		long[] ps = new long[inputLength];
		int i = -1;
		while(mr.advanceLine()){
			i++;
			if(!(i >= garblerId * inputLength && i < (garblerId + 1) * inputLength))
				continue;
			betas[i - (garblerId * inputLength)] = mr.getBETA();
			ses[i - (garblerId * inputLength)] = mr.getSE();
			ps[i - (garblerId * inputLength)] = mr.getP();
		}
		mr.close();
		
		boolean[][][] c = new boolean[3][inputLength][];
		for(i = 0; i < inputLength; ++i) {
			c[0][i] = Utils.fromInt(betas[i], MetaReader.BETA_WIDTH);
			c[1][i] = Utils.fromInt(ses[i], MetaReader.SE_WIDTH);
			c[2][i] = Utils.fromLong(ps[i], MetaReader.P_WIDTH);
		}
		return c;
	}

	@Override
	public Object secureCompute() throws Exception {
		Debugger.setLogFile("./log/" + (env.getParty().equals(Party.Alice) ? "Garbler_" : "Evaluator_") 
				+ machine.getGarblerId() + "_P_Z.log");
		
		long s = System.nanoTime();
		
		/*
		 * Get input from file
		 */
		Debugger.debug(machine.getGarblerId(), env, "Getting input from study file '"+ studyName + "'");
		long timing = System.currentTimeMillis();
		
		int inputLength = machine.getInputLength() / machine.getTotalMachines();
		boolean[][][] data = getInput(inputLength, machine.getGarblerId(), machine.getTotalMachines());
		
		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		
		/*
		 * Transform input into garble circuit signals
		 */
		Debugger.debug(machine.getGarblerId(), env, "Transforming input into garble circuit signals");
		timing = System.currentTimeMillis();
		
		T[][] aliceBetaTData, bobBetaTData, aliceSeTData, bobSeTData, alicePTData, bobPTData;
		aliceBetaTData = env.inputOfAlice(data[0]); //If generator, values in data[0] will be used; if evaluator, only length will be used.
		aliceSeTData = env.inputOfAlice(data[1]);
		alicePTData = env.inputOfAlice(data[2]);
		bobBetaTData = env.inputOfBob(data[0]);
		bobSeTData = env.inputOfBob(data[1]);
		bobPTData = env.inputOfBob(data[2]);
		data = null;
		
		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		
		IntegerLib<T> intLib = new  IntegerLib<T>(env);
		BitonicSortLib<T> sortLib = new BitonicSortLib<T>(env);
		FixedPointLib<T> fpLib = new FixedPointLib<T>(env, MetaReader.BETA_WIDTH, MetaReader.BETA_OFFSET);
		T[][] A_xor_B_P = env.newTArray(alicePTData.length, 0), 
				A_xor_B_BETA = env.newTArray(aliceBetaTData.length, 0), 
				A_xor_B_SE = env.newTArray(aliceSeTData.length, 0), 
				zStats = env.newTArray(aliceBetaTData.length, 0);
		
		/*
		 * XOR the two shares, and compute Z statistics
		 */
		Debugger.debug(machine.getGarblerId(), env, "XORing and computing Z statistics");
		timing = System.currentTimeMillis();
		for(int j = 0; j < A_xor_B_P.length; j++){
			A_xor_B_P[j] = intLib.xor(alicePTData[j], bobPTData[j]);
			A_xor_B_BETA[j] = intLib.xor(aliceBetaTData[j], bobBetaTData[j]);
			A_xor_B_SE[j] = intLib.xor(aliceSeTData[j], bobSeTData[j]);
			/*
			 * z = BETA / SE
			 */
			zStats[j] = intLib.absolute(fpLib.div(A_xor_B_BETA[j], A_xor_B_SE[j]));
		}
		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		aliceBetaTData = bobBetaTData = aliceSeTData = bobSeTData = alicePTData = bobPTData = null;
		A_xor_B_BETA = A_xor_B_SE = null;
		
		/*
		 * Preserve only a predefined number of bits (i.e., the precision) for the P values
		 */
		T[] P_preserved_bits_signal = intLib.toSignals(P_preserved_bits),
				Z_preserved_bits_signal = intLib.toSignals(Z_preserved_bits);
		
		Debugger.debug(machine.getGarblerId(), env, "Truncating precision of P values");
		timing = System.currentTimeMillis();
		for(int j = 0; j < A_xor_B_P.length; j++){
			T reachedOneSignal = intLib.SIGNAL_ZERO;
			T[] curPreservedSignal = intLib.toSignals(0);
			for(int k = A_xor_B_P[j].length - 1; k >= 0; k--){
				T reachedLimit = intLib.eq(curPreservedSignal, P_preserved_bits_signal);
				reachedOneSignal = intLib.or(reachedOneSignal, A_xor_B_P[j][k]);
				T preservedFlag = intLib.and(reachedOneSignal, intLib.not(reachedLimit));
				A_xor_B_P[j][k] = intLib.mux(
						intLib.SIGNAL_ZERO,
						A_xor_B_P[j][k],
						preservedFlag);
				curPreservedSignal = intLib.conditionalIncreament(curPreservedSignal, preservedFlag);
			}
		}
		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		
		/*
		 * Preserve only a predefined number of bits (i.e.e, the precision) for the z statistics
		 */
		Debugger.debug(machine.getGarblerId(), env, "Truncating precision of Z statistics");
		timing = System.currentTimeMillis();
		for(int j = 0; j < zStats.length; j++){
			T reachedOneSignal = intLib.SIGNAL_ZERO;
			T[] curPreservedSignal = intLib.toSignals(0);
			for(int k = zStats[j].length - 1; k >= 0; k--){
				T reachedLimit = intLib.eq(curPreservedSignal, Z_preserved_bits_signal);
				reachedOneSignal = intLib.or(reachedOneSignal, zStats[j][k]);
				T preservedFlag = intLib.and(reachedOneSignal, intLib.not(reachedLimit));
				zStats[j][k] = intLib.mux(
						intLib.SIGNAL_ZERO,
						zStats[j][k],
						preservedFlag);
				curPreservedSignal = intLib.conditionalIncreament(curPreservedSignal, preservedFlag);
			}
		}
		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		
		/*
		 * Concatenate the P values and z statistics
		 */
		Debugger.debug(machine.getGarblerId(), env, "Concatenating P values and Z statistics");
		timing = System.currentTimeMillis();
		T[][] pz = env.newTArray(zStats.length, MetaReader.P_WIDTH + MetaReader.BETA_WIDTH);
		for(int j = 0; j < pz.length; j++){
			System.arraycopy(zStats[j], 0, pz[j], 0, MetaReader.BETA_WIDTH);
			System.arraycopy(A_xor_B_P[j], 0, pz[j], MetaReader.BETA_WIDTH, MetaReader.P_WIDTH);
		}
		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		A_xor_B_P = zStats = null;
		
		/*
		 * Sort the p-z value pairs
		 */
		Debugger.debug(machine.getGarblerId(), env, "Sorting P-Z value pairs");
		timing = System.currentTimeMillis();
		
		DataGraphNode<T>[] nodes = new DataGraphNode[pz.length];
		for (int i = 0; i < nodes.length; i++) {
			nodes[i] = new DataGraphNode<T>(pz[i], env);
		}
		pz = null;
		
		new SortGadget<T>(env, machine)
		.setInputs(nodes, DataGraphNode.getDataComparator(env, MetaReader.P_WIDTH + MetaReader.BETA_WIDTH))
		.secureCompute();
		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		
		/*
		 * De-duplicate
		 */
		Debugger.debug(machine.getGarblerId(), env, "De-duplicating P-Z value pairs");
		timing = System.currentTimeMillis();
		T[] prevPair = nodes[0].getData();
		T[] maxPair = sortLib.ones(nodes[0].getDataLength());
		maxPair[nodes[0].getDataLength() - 1] = sortLib.SIGNAL_ZERO;
		for(int j = 1; j < nodes.length; j++){
			T eqSignal = sortLib.eq(prevPair, nodes[j].getData());
			nodes[j].setData(sortLib.mux(nodes[j].getData(), maxPair, eqSignal));
			prevPair = sortLib.mux(nodes[j].getData(), prevPair, eqSignal);
		}
		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		
		/*
		 * Move all duplicated items to the end
		 */
		Debugger.debug(machine.getGarblerId(), env, "Moving duplicated P-Z value pairs to the end");
		timing = System.currentTimeMillis();
		new SortGadget<T>(env, machine)
		.setInputs(nodes, DataGraphNode.getDataComparator(env, MetaReader.P_WIDTH + MetaReader.BETA_WIDTH))
		.secureCompute();
		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");

		print(machine.getGarblerId(), env, nodes);
		nodes = null;

		long e = System.nanoTime();
		Debugger.debug(machine.getGarblerId(), env, "Total runtime: P-Z runtime " + (e-s)/1e9 + "s");
		
		MemoryHeapMap.printGeneralMemInfo();
		
		return null;
	}
	
//	@Override
//	public Object secureCompute2() throws Exception {
//		long s = System.nanoTime();
//		
//		int inputLength = machine.getInputLength() / machine.getTotalMachines();
//		boolean[][][] data = getInput(inputLength, machine.getGarblerId(), machine.getTotalMachines());
//		
//		Debugger.debug(machine.getGarblerId(), env, "Preparing input from study file '"+ studyName + "'");
//		
//		T[][] aliceBetaTData, bobBetaTData, aliceSeTData, bobSeTData, alicePTData, bobPTData;
//		if(env.getParty().equals(Party.Alice)){
//			aliceBetaTData = env.inputOfAlice(data[0]);
//			aliceSeTData = env.inputOfAlice(data[1]);
//			alicePTData = env.inputOfAlice(data[2]);
//			bobBetaTData = env.inputOfBob(new boolean[data[0].length][MetaReader.BETA_WIDTH]);
//			bobSeTData = env.inputOfBob(new boolean[data[1].length][MetaReader.SE_WIDTH]);
//			bobPTData = env.inputOfBob(new boolean[data[2].length][MetaReader.P_WIDTH]);
//		}
//		else{
//			aliceBetaTData = env.inputOfAlice(new boolean[data[0].length][MetaReader.BETA_WIDTH]);
//			aliceSeTData = env.inputOfAlice(new boolean[data[1].length][MetaReader.SE_WIDTH]);
//			alicePTData = env.inputOfAlice(new boolean[data[2].length][MetaReader.P_WIDTH]);
//			bobBetaTData = env.inputOfBob(data[0]);
//			bobSeTData = env.inputOfBob(data[1]);
//			bobPTData = env.inputOfBob(data[2]);
//		}
//		
//		Debugger.debug(machine.getGarblerId(), env, "END preparing input from study file '"+ studyName + "'");
//		
//		IntegerLib<T> intLib = new  IntegerLib<T>(env);
//		BitonicSortLib<T> sortLib = new BitonicSortLib<T>(env);
//		FixedPointLib<T> fpLib = new FixedPointLib<T>(env, MetaReader.BETA_WIDTH, MetaReader.BETA_OFFSET);
//		T[][] A_xor_B_P = env.newTArray(alicePTData.length, 0), 
//				A_xor_B_BETA = env.newTArray(aliceBetaTData.length, 0), 
//				A_xor_B_SE = env.newTArray(aliceSeTData.length, 0), 
//				zStats = env.newTArray(aliceBetaTData.length, 0);
//		
//		/*
//		 * XOR the two shares
//		 */
//		Debugger.debug(machine.getGarblerId(), env, "XORing and computing Z statistics");
//		long timing = System.currentTimeMillis();
//		for(int j = 0; j < A_xor_B_P.length; j++){
//			A_xor_B_P[j] = intLib.xor(alicePTData[j], bobPTData[j]);
//			A_xor_B_BETA[j] = intLib.absolute(intLib.xor(aliceBetaTData[j], bobBetaTData[j]));
//			A_xor_B_SE[j] = intLib.xor(aliceSeTData[j], bobSeTData[j]);
//		}
//		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
//		
//		
//		/*
//		 * Preserve only a predefined number of bits (i.e., the precision) for the P values
//		 */
//		T[] P_preserved_bits_signal = intLib.toSignals(P_preserved_bits),
//				Z_preserved_bits_signal = intLib.toSignals(Z_preserved_bits);
//		
//		Debugger.debug(machine.getGarblerId(), env, "Truncating precision of P values");
//		timing = System.currentTimeMillis();
//		for(int j = 0; j < A_xor_B_P.length; j++){
//			T reachedOneSignal = intLib.SIGNAL_ZERO;
//			T[] curPreservedSignal = intLib.toSignals(0);
//			for(int k = A_xor_B_P[j].length - 1; k >= 0; k--){
//				T reachedLimit = intLib.eq(curPreservedSignal, P_preserved_bits_signal);
//				reachedOneSignal = intLib.or(reachedOneSignal, A_xor_B_P[j][k]);
//				T preservedFlag = intLib.and(reachedOneSignal, intLib.not(reachedLimit));
//				A_xor_B_P[j][k] = intLib.mux(
//						intLib.SIGNAL_ZERO,
//						A_xor_B_P[j][k],
//						preservedFlag);
//				curPreservedSignal = intLib.conditionalIncreament(curPreservedSignal, preservedFlag);
//			}
//		}
//		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
//		
//		/*
//		 * Preserve only a predefined number of bits (i.e.e, the precision) for the beta estimates
//		 */
//		Debugger.debug(machine.getGarblerId(), env, "Truncating precision of beta estimates");
//		timing = System.currentTimeMillis();
//		for(int j = 0; j < A_xor_B_BETA.length; j++){
//			T reachedOneSignal = intLib.SIGNAL_ZERO;
//			T[] curPreservedSignal = intLib.toSignals(0);
//			for(int k = A_xor_B_BETA[j].length - 1; k >= 0; k--){
//				T reachedLimit = intLib.eq(curPreservedSignal, Z_preserved_bits_signal);
//				reachedOneSignal = intLib.or(reachedOneSignal, A_xor_B_BETA[j][k]);
//				T preservedFlag = intLib.and(reachedOneSignal, intLib.not(reachedLimit));
//				A_xor_B_BETA[j][k] = intLib.mux(
//						intLib.SIGNAL_ZERO,
//						A_xor_B_BETA[j][k],
//						preservedFlag);
//				curPreservedSignal = intLib.conditionalIncreament(curPreservedSignal, preservedFlag);
//			}
//		}
//		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
//		
//		/*
//		 * Preserve only a predefined number of bits (i.e.e, the precision) for the standard errors
//		 */
//		Debugger.debug(machine.getGarblerId(), env, "Truncating precision of standard errors");
//		timing = System.currentTimeMillis();
//		for(int j = 0; j < A_xor_B_SE.length; j++){
//			T reachedOneSignal = intLib.SIGNAL_ZERO;
//			T[] curPreservedSignal = intLib.toSignals(0);
//			for(int k = A_xor_B_SE[j].length - 1; k >= 0; k--){
//				T reachedLimit = intLib.eq(curPreservedSignal, Z_preserved_bits_signal);
//				reachedOneSignal = intLib.or(reachedOneSignal, A_xor_B_SE[j][k]);
//				T preservedFlag = intLib.and(reachedOneSignal, intLib.not(reachedLimit));
//				A_xor_B_SE[j][k] = intLib.mux(
//						intLib.SIGNAL_ZERO,
//						A_xor_B_SE[j][k],
//						preservedFlag);
//				curPreservedSignal = intLib.conditionalIncreament(curPreservedSignal, preservedFlag);
//			}
//		}
//		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
//		
//		/*
//		 * Concatenate P values, Beta estimates, and standard errors
//		 */
//		Debugger.debug(machine.getGarblerId(), env, "Concatenating P values, Beta estimates, and standard errors");
//		timing = System.currentTimeMillis();
//		T[][] pbs = env.newTArray(A_xor_B_P.length, MetaReader.P_WIDTH + MetaReader.BETA_WIDTH + MetaReader.SE_WIDTH);
//		for(int j = 0; j < pbs.length; j++){
//			System.arraycopy(A_xor_B_SE[j], 0, pbs[j], 0, MetaReader.SE_WIDTH);
//			System.arraycopy(A_xor_B_BETA[j], 0, pbs[j], MetaReader.SE_WIDTH, MetaReader.BETA_WIDTH);
//			System.arraycopy(A_xor_B_P[j], 0, pbs[j], MetaReader.SE_WIDTH + MetaReader.BETA_WIDTH, MetaReader.P_WIDTH);
//		}
//		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
//		
//		/*
//		 * Sort the P-Beta-SE value pairs
//		 */
//		Debugger.debug(machine.getGarblerId(), env, "Sorting P-Beta-SE value pairs");
//		timing = System.currentTimeMillis();
//		
//		DataGraphNode<T>[] nodes = new DataGraphNode[pbs.length];
//		for (int i = 0; i < nodes.length; i++) {
//			nodes[i] = new DataGraphNode<T>(pbs[i], env);
//		}
//		
//		new SortGadget<T>(env, machine)
//		.setInputs(nodes, DataGraphNode.getDataComparator(env, pbs[0].length))
//		.secureCompute();
//		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
//		
//		/*
//		 * De-duplicate
//		 */
//		Debugger.debug(machine.getGarblerId(), env, "De-duplicating P-Beta-SE value pairs");
//		timing = System.currentTimeMillis();
//		T[] uniqueNum = intLib.toSignals(1);
//		T[] prevPair = nodes[0].getData();
//		T[] maxPair = sortLib.ones(nodes[0].getDataLength());
//		maxPair[nodes[0].getDataLength() - 1] = sortLib.SIGNAL_ZERO;
//		for(int j = 1; j < nodes.length; j++){
//			T eqSignal = sortLib.eq(prevPair, nodes[j].getData());
//			nodes[j].setData(sortLib.mux(nodes[j].getData(), maxPair, eqSignal));
//			prevPair = sortLib.mux(nodes[j].getData(), prevPair, eqSignal);
//			uniqueNum = intLib.conditionalIncreament(uniqueNum, intLib.not(eqSignal));
//		}
//		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
//		
//		/*
//		 * Move all duplicated items to the end
//		 */
//		Debugger.debug(machine.getGarblerId(), env, "Moving duplicated P-Z value pairs to the end");
//		timing = System.currentTimeMillis();
//		new SortGadget<T>(env, machine)
//		.setInputs(nodes, DataGraphNode.getDataComparator(env, pbs[0].length))
//		.secureCompute();
//		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
//		
//		/*
//		 * Reveal unique pair number
//		 */
//		int aliceN = Utils.toInt(env.outputToAlice(uniqueNum)), bobN = Utils.toInt(env.outputToBob(uniqueNum));
//		int n = (env.getParty().equals(Party.Alice) ? aliceN : bobN);
//		System.out.println("Unique pair number: " + n);
//		
//		/*
//		 * Compute z statistics
//		 */
//		Debugger.debug(machine.getGarblerId(), env, "Computing z statistics");
//		timing = System.currentTimeMillis();
//		T[] tmpBeta = env.newTArray(MetaReader.BETA_WIDTH),
//				tmpSE = env.newTArray(MetaReader.SE_WIDTH);
//		for(int i = 0; i < n; i++){
//			/*
//			 * z = BETA / SE
//			 */
//			System.arraycopy(nodes[i].getData(), 0, tmpSE, 0, MetaReader.SE_WIDTH);
//			System.arraycopy(nodes[i].getData(), MetaReader.SE_WIDTH, tmpBeta, 0, MetaReader.BETA_WIDTH);
//			zStats[i] = intLib.absolute(fpLib.div(tmpBeta, tmpSE));
//		}
//		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
//		
//		/*
//		 * Concatenate p and z
//		 */
//		Debugger.debug(machine.getGarblerId(), env, "Concatenating p and z");
//		timing = System.currentTimeMillis();
//		DataGraphNode<T>[] newNodes = new DataGraphNode[n];
//		for(int i = 0; i < n; i++){
//			T[] tmpData = env.newTArray(MetaReader.P_WIDTH + MetaReader.SE_WIDTH);
//			System.arraycopy(zStats[i], 0, tmpData, 0, MetaReader.SE_WIDTH);
//			System.arraycopy(nodes[i].getData(), MetaReader.SE_WIDTH + MetaReader.BETA_WIDTH, tmpData, MetaReader.SE_WIDTH, MetaReader.P_WIDTH);
//			newNodes[i] = new DataGraphNode<T>(tmpData, env);
//		}
//		Debugger.debug(machine.getGarblerId(), env, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
//
//		print(machine.getGarblerId(), env, newNodes);
//
//		long e = System.nanoTime();
//		System.out.println((env.getParty().equals(Party.Alice) ? "Garbler " : "Evaluator ") 
//				+ machine.getGarblerId() + ": P-Z runtime " + (e-s)/1e9 + "s");
//		
//		return null;
//	}

	private void print(int garblerId,
			final CompEnv<T> env,
			DataGraphNode<T>[] nodes) throws IOException, BadLabelException {
		NormalDistribution nd = new NormalDistribution();
		BufferedWriter bw = null;
		if (Party.Alice.equals(env.getParty())) {
			 bw = new BufferedWriter(new FileWriter("out/P_Z_" + machine.getInputLength() + ".out." + garblerId));
		}
		for(int i = 0; i < nodes.length; i++){
			boolean[] plainPZ = env.outputToAlice(nodes[i].getData());
			Double zStat = Utils.toFixPoint(Arrays.copyOfRange(plainPZ, 0, MetaReader.SE_WIDTH), MetaReader.SE_OFFSET);
			Double pValue = Utils.toFixPoint(Arrays.copyOfRange(plainPZ, MetaReader.SE_WIDTH, MetaReader.SE_WIDTH + MetaReader.P_WIDTH), MetaReader.P_OFFSET);
			if (Party.Alice.equals(env.party)) {
				bw.write(pValue + "\t\t" + nd.cumulativeProbability(-zStat)*2 + "\n");
			}
		}
		env.channel.flush();
		if(bw != null){
			bw.flush();
			bw.close();
		}
	}

}
