package ch.epfl.lca.genopri.secure;

import java.math.BigInteger;
import java.util.logging.Level;
import java.util.logging.Logger;


import util.EvaRunnable;
import util.GenRunnable;
import util.Utils;
import circuits.BitonicSortLib;
import circuits.arithmetic.FixedPointLib;
import flexsc.CompEnv;

public class Benchmark_Processor {
	private static Logger logger = Logger.getLogger(Benchmark_Processor.class.getName());
	private static int benchmarkSize = 1000;
	private static int bitLen = 32; 
	
	static public<T> T[][] compute(CompEnv<T> gen, T[][] inputs){
		BitonicSortLib<T> sortLib = new  BitonicSortLib<T>(gen);
		FixedPointLib<T> fpLib = new FixedPointLib<T>(gen, bitLen, bitLen/2);
		
		long timing = System.currentTimeMillis();
		/*
		 * Oblivious sorting
		 */
		logger.log(Level.INFO, "============== Oblivious sorting ==============");
		timing = System.currentTimeMillis();
		sortLib.sort(inputs, sortLib.SIGNAL_ONE);
		logger.log(Level.INFO, "============== Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds ==============");
		
		/*
		 * Secure division
		 */
		logger.log(Level.INFO, "============== Secure division ==============");
		timing = System.currentTimeMillis();
		for(int j = 0; j < inputs.length; j++){
			fpLib.div(inputs[j], inputs[j]);
		}
		logger.log(Level.INFO, "============== Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds ==============");
		
		/*
		 * Precision reduction
		 */
		logger.log(Level.INFO, "============== Precision reduction ==============");
		T[] P_preserved_bits_signal = sortLib.toSignals(10);
		
		timing = System.currentTimeMillis();
		for(int j = 0; j < inputs.length; j++){
			T reachedOneSignal = sortLib.SIGNAL_ZERO;
			T[] curPreservedSignal = sortLib.toSignals(0);
			for(int k = inputs[j].length - 1; k >= 0; k--){
				T reachedLimit = sortLib.eq(curPreservedSignal, P_preserved_bits_signal);
				reachedOneSignal = sortLib.or(reachedOneSignal, inputs[j][k]);
				T preservedFlag = sortLib.and(reachedOneSignal, sortLib.not(reachedLimit));
				inputs[j][k] = sortLib.mux(
						sortLib.SIGNAL_ZERO,
						inputs[j][k],
						preservedFlag);
				curPreservedSignal = sortLib.conditionalIncreament(curPreservedSignal, preservedFlag);
			}
		}
		logger.log(Level.INFO, "============== Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds ==============");
				
		/*
		 * De-duplicate
		 */
		logger.log(Level.INFO, "============== De-duplication ==============");
		timing = System.currentTimeMillis();
		T[] prevPair = inputs[0];
		T[] maxPair = sortLib.ones(inputs[0].length);
		maxPair[inputs[0].length - 1] = sortLib.SIGNAL_ZERO;
		for(int j = 1; j < inputs.length; j++){
			T eqSignal = sortLib.eq(prevPair, inputs[j]);
			inputs[j] = sortLib.mux(inputs[j], maxPair, eqSignal);
			prevPair = sortLib.mux(inputs[j], prevPair, eqSignal);
		}
		logger.log(Level.INFO, "============== Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds ==============");
		
		return null;
	}

	public static class Generator<T> extends GenRunnable<T>{
		
		/** Generator's input  */
		T[][] inputs;
		
		@Override
		public void prepareInput(CompEnv<T> gen) throws Exception {
			logger.log(Level.INFO, "++++++++++ Generator: Preparing input ++++++++++");
			
			bitLen = Integer.valueOf(args[0]);
			inputs = gen.inputOfBob(new boolean[benchmarkSize][bitLen]);
			
			logger.log(Level.INFO, "---------- Generator: End preparing input ----------");
		}

		@Override
		public void secureCompute(CompEnv<T> gen) throws Exception {
			logger.log(Level.INFO, "++++++++++ Generator: Computing ++++++++++");
			
			compute(gen, inputs);
			
			logger.log(Level.INFO, "---------- Generator: End computing ----------");
		}

		@Override
		public void prepareOutput(CompEnv<T> gen) throws Exception {
			
		}
	}
	
	public static class Evaluator<T> extends EvaRunnable<T>{
		
		/** Evaluator's input  */
		T[][] inputs;
		
		@Override
		public void prepareInput(CompEnv<T> gen) throws Exception {
			logger.log(Level.INFO, "++++++++++ Evaluator: Preparing input ++++++++++");
			
			bitLen = Integer.valueOf(args[0]);
			boolean[][] temp = new boolean[benchmarkSize][];
			for(int i = 0; i < temp.length; i++)
				temp[i] = Utils.fromBigInteger(new BigInteger("0"), bitLen);
			inputs = gen.inputOfBob(temp);
			
			logger.log(Level.INFO, "---------- Evaluator: End preparing input ----------");
		}

		@Override
		public void secureCompute(CompEnv<T> gen) throws Exception {
			logger.log(Level.INFO, "++++++++++ Evaluator: Computing ++++++++++");
			
			compute(gen, inputs);
			
			logger.log(Level.INFO, "---------- Evaluator: End computing ----------");
		}

		@Override
		public void prepareOutput(CompEnv<T> gen) throws Exception {
		}
		
	}

}
