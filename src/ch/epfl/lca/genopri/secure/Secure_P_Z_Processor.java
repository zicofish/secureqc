package ch.epfl.lca.genopri.secure;

import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.logging.Level;
import java.util.logging.Logger;

import org.apache.commons.math3.distribution.NormalDistribution;

import util.EvaRunnable;
import util.GenRunnable;
import util.Utils;
import circuits.BitonicSortLib;
import circuits.arithmetic.FixedPointLib;
import flexsc.CompEnv;


public class Secure_P_Z_Processor extends SecureMetaProcessor{
	private static Logger logger = Logger.getLogger(Secure_P_Z_Processor.class.getName());
	
	private static final int P_preserved_bits = 10;
	
	private static final int Z_preserved_bits = 10;
	
	protected Secure_P_Z_Processor(File study) {
		super(study);
	}
	
	static public<T> T[][] compute(CompEnv<T> gen, 
			T[][] inputA_P, T[][] inputA_BETA, T[][] inputA_SE, 
			T[][] inputB_P, T[][] inputB_BETA, T[][] inputB_SE){
		// Because BitonicSortLib extends the IntegerLib, we use it for all operations except fix-point computation.
		BitonicSortLib<T> sortLib = new  BitonicSortLib<T>(gen);
		FixedPointLib<T> fpLib = new FixedPointLib<T>(gen, BETA_WIDTH, BETA_OFFSET);
		T[][] A_xor_B_P = gen.newTArray(inputA_P.length, inputA_P[0].length),
				A_xor_B_BETA = gen.newTArray(inputA_BETA.length, inputA_BETA[0].length),
				A_xor_B_SE = gen.newTArray(inputA_SE.length, inputA_SE[0].length),
				zStats = gen.newTArray(inputA_BETA.length, inputB_BETA[0].length);
		
		/*
		 * XOR the two shares, and compute Z statistics
		 */
		logger.log(Level.INFO, "============== XORing and computing Z statistics ==============");
		long timing = System.currentTimeMillis();
		for(int j = 0; j < inputA_P.length; j++){
			A_xor_B_P[j] = sortLib.xor(inputA_P[j], inputB_P[j]);
			A_xor_B_BETA[j] = sortLib.xor(inputA_BETA[j], inputB_BETA[j]);
			A_xor_B_SE[j] = sortLib.xor(inputA_SE[j], inputB_SE[j]);
			/*
			 * z = BETA / SE
			 */
			zStats[j] = sortLib.absolute(fpLib.div(A_xor_B_BETA[j], A_xor_B_SE[j]));
		}
		logger.log(Level.INFO, "============== Timing:  " + (System.currentTimeMillis() - timing) / 1000 +  " seconds ==============");
		T[] P_preserved_bits_signal = sortLib.toSignals(P_preserved_bits),
				Z_preserved_bits_signal = sortLib.toSignals(Z_preserved_bits);
		
		/*
		 * Preserve only a predefined number of bits (i.e., the precision) for the P values
		 */
		logger.log(Level.INFO, "============== Truncating precision of P values ==============");
		timing = System.currentTimeMillis();
		for(int j = 0; j < A_xor_B_P.length; j++){
			T reachedOneSignal = sortLib.SIGNAL_ZERO;
			T[] curPreservedSignal = sortLib.toSignals(0);
			for(int k = A_xor_B_P[j].length - 1; k >= 0; k--){
				T reachedLimit = sortLib.eq(curPreservedSignal, P_preserved_bits_signal);
				reachedOneSignal = sortLib.or(reachedOneSignal, A_xor_B_P[j][k]);
				T preservedFlag = sortLib.and(reachedOneSignal, sortLib.not(reachedLimit));
				A_xor_B_P[j][k] = sortLib.mux(
						sortLib.SIGNAL_ZERO,
						A_xor_B_P[j][k],
						preservedFlag);
				curPreservedSignal = sortLib.conditionalIncreament(curPreservedSignal, preservedFlag);
			}
		}
		logger.log(Level.INFO, "============== Timing:  " + (System.currentTimeMillis() - timing) / 1000 +  " seconds ==============");
		
		/*
		 * Preserve only a predefined number of bits (i.e.e, the precision) for the z statistics
		 */
		logger.log(Level.INFO, "============== Truncating precision of Z statistics ==============");
		timing = System.currentTimeMillis();
		for(int j = 0; j < zStats.length; j++){
			T reachedOneSignal = sortLib.SIGNAL_ZERO;
			T[] curPreservedSignal = sortLib.toSignals(0);
			for(int k = zStats[j].length - 1; k >= 0; k--){
				T reachedLimit = sortLib.eq(curPreservedSignal, Z_preserved_bits_signal);
				reachedOneSignal = sortLib.or(reachedOneSignal, zStats[j][k]);
				T preservedFlag = sortLib.and(reachedOneSignal, sortLib.not(reachedLimit));
				zStats[j][k] = sortLib.mux(
						sortLib.SIGNAL_ZERO,
						zStats[j][k],
						preservedFlag);
				curPreservedSignal = sortLib.conditionalIncreament(curPreservedSignal, preservedFlag);
			}
		}
		logger.log(Level.INFO, "============== Timing:  " + (System.currentTimeMillis() - timing) / 1000 +  " seconds ==============");
		
		/*
		 * Concatenate the P values and z statistics
		 */
		logger.log(Level.INFO, "============== Concatenating P values and Z statistics ==============");
		timing = System.currentTimeMillis();
		T[][] pz = gen.newTArray(zStats.length, A_xor_B_P[0].length + zStats[0].length);
		for(int j = 0; j < pz.length; j++){
			System.arraycopy(zStats[j], 0, pz[j], 0, zStats[j].length);
			System.arraycopy(A_xor_B_P[j], 0, pz[j], zStats[j].length, A_xor_B_P[j].length);
		}
		logger.log(Level.INFO, "============== Timing:  " + (System.currentTimeMillis() - timing) / 1000 +  " seconds ==============");
		
		/*
		 * Sort the p-z value pairs
		 */
		logger.log(Level.INFO, "============== Sorting P-Z value pairs ==============");
		timing = System.currentTimeMillis();
		sortLib.sort(pz, sortLib.SIGNAL_ONE);
		logger.log(Level.INFO, "============== Timing:  " + (System.currentTimeMillis() - timing) / 1000 +  " seconds ==============");
		
		/*
		 * De-duplicate
		 */
		logger.log(Level.INFO, "============== De-duplicating P-Z value pairs ==============");
		timing = System.currentTimeMillis();
		T[] prevPair = pz[0];
		T[] maxPair = sortLib.ones(pz[0].length);
		maxPair[pz[0].length - 1] = sortLib.SIGNAL_ZERO;
		for(int j = 1; j < pz.length; j++){
			T eqSignal = sortLib.eq(prevPair, pz[j]);
			pz[j] = sortLib.mux(pz[j], maxPair, eqSignal);
			prevPair = sortLib.mux(pz[j], prevPair, eqSignal);
		}
		logger.log(Level.INFO, "============== Timing:  " + (System.currentTimeMillis() - timing) / 1000 +  " seconds ==============");
		
		/*
		 * Move all duplicated items to the end
		 */
		logger.log(Level.INFO, "============== Moving duplicated P-Z value pairs to the end ==============");
		timing = System.currentTimeMillis();
		sortLib.sort(pz, sortLib.SIGNAL_ONE);
		logger.log(Level.INFO, "============== Timing:  " + (System.currentTimeMillis() - timing) / 1000 +  " seconds ==============");
		
		/* We could also trim the duplicated items, but that requires another round of secure computation,
		 * we would like to avoid that. We just return the entire results and let the user delete those elements
		 * once the results are revealed.
		 */
		
		return pz;
	}

	public static class Generator<T> extends GenRunnable<T>{
		
		/** The study */
		String studyName;

		/** Generator's input (list of reported p-value shares, beta shares, and standard error shares) */
		T[][] inputA_P, inputA_BETA, inputA_SE;
		
		/** Evaluator's input. Because this class is a Generator, inputB will contain random elements. */
		T[][] inputB_P, inputB_BETA, inputB_SE;
		
		/** The sorted and de-duplicated P-value and Z-statistics pairs */
		T[][] pz;
		
		@Override
		public void prepareInput(CompEnv<T> gen) throws Exception {
			studyName = args[0];
			SecureMetaProcessor smp = new Secure_P_Z_Processor(new File(studyName));
			logger.log(Level.INFO, "++++++++++ Generator: Preparing input from study file '"
					+ studyName
					+ "' ++++++++++");
			
			ArrayList<Integer> BETAs = new ArrayList<>(APPROX_SIZE), SEs = new ArrayList<>(APPROX_SIZE);
			ArrayList<Long> Ps = new ArrayList<>(APPROX_SIZE);
			while(smp.advanceLine()){
				BETAs.add(smp.getBETA());
				SEs.add(smp.getSE());
				Ps.add(smp.getP());
			}
			smp.closeStudy();
			boolean[][] temp = new boolean[BETAs.size()][];
			for(int i = 0; i < temp.length; i++)
				temp[i] = Utils.fromLong(Ps.get(i), P_WIDTH);
			inputA_P = gen.inputOfAlice(temp);
			inputB_P = gen.inputOfBob(temp); // inputOfBob only uses the dimension information of temp.
			
			for(int i = 0; i < temp.length; i++)
				temp[i] = Utils.fromInt(BETAs.get(i), BETA_WIDTH);
			inputA_BETA = gen.inputOfAlice(temp);
			inputB_BETA = gen.inputOfBob(temp);
			
			for(int i = 0; i < temp.length; i++)
				temp[i] = Utils.fromInt(SEs.get(i), SE_WIDTH);
			inputA_SE = gen.inputOfAlice(temp);
			inputB_SE = gen.inputOfBob(temp);
			
			logger.log(Level.INFO, "---------- Generator: End preparing input ----------");
		}

		@Override
		public void secureCompute(CompEnv<T> gen) throws Exception {
			logger.log(Level.INFO, "++++++++++ Generator: Computing P-Z value pairs ++++++++++");
			
			pz = compute(gen, inputA_P, inputA_BETA, inputA_SE, inputB_P, inputB_BETA, inputB_SE);
			
			logger.log(Level.INFO, "---------- Generator: End computing ----------");
		}

		@Override
		public void prepareOutput(CompEnv<T> gen) throws Exception {
			NormalDistribution nd = new NormalDistribution();
			for(int i = 0; i < pz.length; i++){
				boolean[] plainPZ = gen.outputToAlice(pz[i]);
				Double zStat = Utils.toFixPoint(Arrays.copyOfRange(plainPZ, 0, SE_WIDTH), SE_OFFSET);
				Double pValue = Utils.toFixPoint(Arrays.copyOfRange(plainPZ, SE_WIDTH, SE_WIDTH + P_WIDTH), P_OFFSET);
				System.out.println(pValue + "------" + nd.cumulativeProbability(-zStat)*2);
			}
//			logger.log(Level.INFO, "========== Generator: median SE is " + Utils.toFixPoint(plainMedian, 24) + " ==========");
		}
	}
	
	public static class Evaluator<T> extends EvaRunnable<T>{
		
		/** The study */
		String studyName;

		/** Generator's input. Because this class is an Evaluator, inputA will contain random elements.   */
		T[][] inputA_P, inputA_BETA, inputA_SE;
		
		/** Evaluator's input (list of reported p-value shares, beta shares, and standard error shares). */
		T[][] inputB_P, inputB_BETA, inputB_SE;
		
		/** The sorted and de-duplicated P-value and Z-statistics pairs */
		T[][] pz;
		
		@Override
		public void prepareInput(CompEnv<T> gen) throws Exception {
			studyName = args[0];
			SecureMetaProcessor smp = new Secure_P_Z_Processor(new File(studyName));
			logger.log(Level.INFO, "++++++++++ Evaluator: Preparing input from study file '"
					+ studyName
					+ "' ++++++++++");
			
			ArrayList<Integer> BETAs = new ArrayList<>(APPROX_SIZE), SEs = new ArrayList<>(APPROX_SIZE);
			ArrayList<Long> Ps = new ArrayList<>(APPROX_SIZE);
			while(smp.advanceLine()){
				BETAs.add(smp.getBETA());
				SEs.add(smp.getSE());
				Ps.add(smp.getP());
			}
			smp.closeStudy();
			boolean[][] temp = new boolean[BETAs.size()][];
			for(int i = 0; i < temp.length; i++)
				temp[i] = Utils.fromLong(Ps.get(i), P_WIDTH);
			inputA_P = gen.inputOfAlice(temp); // inputOfAlice only uses the dimension information of temp.
			inputB_P = gen.inputOfBob(temp); 
			
			for(int i = 0; i < temp.length; i++)
				temp[i] = Utils.fromInt(BETAs.get(i), BETA_WIDTH);
			inputA_BETA = gen.inputOfAlice(temp);
			inputB_BETA = gen.inputOfBob(temp);
			
			for(int i = 0; i < temp.length; i++)
				temp[i] = Utils.fromInt(SEs.get(i), SE_WIDTH);
			inputA_SE = gen.inputOfAlice(temp);
			inputB_SE = gen.inputOfBob(temp);
			
			logger.log(Level.INFO, "---------- Evaluator: End preparing input ----------");
		}

		@Override
		public void secureCompute(CompEnv<T> gen) throws Exception {
			logger.log(Level.INFO, "++++++++++ Evaluator: Computing P-Z value pairs ++++++++++");
			
			pz = compute(gen, inputA_P, inputA_BETA, inputA_SE, inputB_P, inputB_BETA, inputB_SE);
			
			logger.log(Level.INFO, "---------- Evaluator: End computing ----------");
		}

		@Override
		public void prepareOutput(CompEnv<T> gen) throws Exception {
			for(int i = 0; i < pz.length; i++)
				gen.outputToAlice(pz[i]);
		}
		
	}
}
