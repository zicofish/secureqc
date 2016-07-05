package ch.epfl.lca.genopri.secure;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;
import java.util.logging.Level;
import java.util.logging.Logger;

import util.EvaRunnable;
import util.GenRunnable;
import util.Utils;
import ch.epfl.lca.genopri.secure.parallel.DifferentialPrivacy;
import ch.epfl.lca.genopri.secure.parallel.RefAFReader;
import circuits.BitonicSortLib;
import circuits.arithmetic.IntegerLib;
import flexsc.CompEnv;


public class Secure_EAF_Processor extends MetaReader{
	private static Logger logger = Logger.getLogger(Secure_EAF_Processor.class.getName());
	
	private static int EAF_preserved_bits = MetaReader.EAF_WIDTH - MetaReader.EAF_OFFSET + 7; 
			
	private static int testSize = 8000;
	
	
	protected Secure_EAF_Processor(File study) throws IOException {
		super(study);
	}
	
	static public<T> T[][] compute(CompEnv<T> env, 
			boolean[][][] data){
		BitonicSortLib<T> sortLib = new  BitonicSortLib<T>(env);
		IntegerLib<T> intLib = new  IntegerLib<T>(env);
		T[][] aliceEafTData, bobEafTData, A_xor_B_EAF, refEAF, aliceNoises, bobNoises, eafPairs;
		T[] zeroEAF, oneEAF, prevPair, maxPair;
		
		/*
		 * Transform input into garble circuit signals
		 */
		
		logger.log(Level.INFO, "Transforming input into garble circuit signals");
		long timing = System.currentTimeMillis();
		
		aliceEafTData = env.inputOfAlice(data[0]);
		bobEafTData = env.inputOfBob(data[0]);
		
		logger.log(Level.INFO, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		
		
		A_xor_B_EAF = env.newTArray(aliceEafTData.length, 0);
		refEAF = env.newTArray(aliceEafTData.length, 0);
		
		/*
		 * XOR the two shares
		 */
		logger.log(Level.INFO, "XORing EAF");
		timing = System.currentTimeMillis();
		for(int j = 0; j < A_xor_B_EAF.length; j++){
			A_xor_B_EAF[j] = intLib.xor(aliceEafTData[j], bobEafTData[j]);
			if(data[1][j] != null)
				refEAF[j] = env.inputOfAlice(data[1][j]);
			else
				refEAF[j] = intLib.xor(aliceEafTData[j], bobEafTData[j]);
		}
		logger.log(Level.INFO, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		data = null;
		aliceEafTData = null;
		bobEafTData = null;
		
		/*
		 * Add differential privacy noise to study EAF
		 */
		logger.log(Level.INFO, "Adding differential privacy noises");
		timing = System.currentTimeMillis();
		double sensitivity = 1.0 / 1000;
	    double epsilon = 0.1;
	    double delta = 0.05;
	    DifferentialPrivacy dp = new DifferentialPrivacy(sensitivity, epsilon, delta);
	    double[] noises = dp.genNoises(A_xor_B_EAF.length, "gaussian");
	    boolean[][] fpNoises = new boolean[noises.length][];
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
		logger.log(Level.INFO, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		aliceNoises = null;
		bobNoises = null;
		fpNoises = null;
		noises = null;
		dp = null;
		
		/*
		 * Preserve only a predefined number of bits (i.e., the precision) for the EAF values,
		 * and concatenate the truncated study EAF and reference EAF
		 */
		
		logger.log(Level.INFO, "Truncating precision of EAF values");
		timing = System.currentTimeMillis();
		eafPairs = env.newTArray(refEAF.length, EAF_preserved_bits * 2);
		for(int j = 0; j < A_xor_B_EAF.length; j++){
			System.arraycopy(refEAF[j], MetaReader.EAF_WIDTH - EAF_preserved_bits, eafPairs[j], 0, EAF_preserved_bits);
			System.arraycopy(A_xor_B_EAF[j], MetaReader.EAF_WIDTH - EAF_preserved_bits, eafPairs[j], EAF_preserved_bits, EAF_preserved_bits);
		}
		logger.log(Level.INFO, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		A_xor_B_EAF = null;
		refEAF = null;
		
		/*
		 * Sort the EAF value pairs
		 */
		logger.log(Level.INFO, "Sorting EAF value pairs");
		timing = System.currentTimeMillis();
		sortLib.sort(eafPairs, sortLib.SIGNAL_ONE);
		logger.log(Level.INFO, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		
		/*
		 * De-duplicate
		 */
		logger.log(Level.INFO, "De-duplicating EAF value pairs");
		timing = System.currentTimeMillis();
		prevPair = eafPairs[0];
		maxPair = intLib.ones(eafPairs[0].length);
		maxPair[eafPairs[0].length - 1] = intLib.SIGNAL_ZERO;
		for(int j = 1; j < eafPairs.length; j++){
			T eqSignal = intLib.eq(prevPair, eafPairs[j]);
			eafPairs[j] = intLib.mux(eafPairs[j], maxPair, eqSignal);
			prevPair = intLib.mux(eafPairs[j], prevPair, eqSignal);
		}
		logger.log(Level.INFO, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		prevPair = null;
		maxPair = null;
		
		/*
		 * Move all duplicated items to the end
		 */
		logger.log(Level.INFO, "Moving duplicated EAF value pairs to the end");
		timing = System.currentTimeMillis();
		sortLib.sort(eafPairs, sortLib.SIGNAL_ONE);
		logger.log(Level.INFO, "Timing:  " + (System.currentTimeMillis() - timing) / 1000.0 +  " seconds");
		
		/* We could also trim the duplicated items, but that requires another round of secure computation,
		 * we would like to avoid that. We just return the entire results and let the user delete those elements
		 * once the results are revealed.
		 */
		
		return eafPairs;
	}

	public static class Generator<T> extends GenRunnable<T>{
		
		/** The study */
		String studyName;
		
		/** The reference*/
		String refName = "../data/reference/aligned_AlleleFreq_HapMap_CEU_phase3.2_nr.b36_fwd.txt";
		
		boolean[][][] EAFPairs;
		
		T[][] result;
		
		@Override
		public void prepareInput(CompEnv<T> gen) throws Exception {
			studyName = args[0];
			MetaReader mr = new Secure_EAF_Processor(new File(studyName));
			RefAFReader rar = new RefAFReader(new File(refName));
			
			logger.log(Level.INFO, "++++++++++ Generator: Preparing input from study file '"
					+ studyName
					+ "' ++++++++++");
			
			EAFPairs = new boolean[2][testSize][];
			int tmp = 0;
			char refAllele, otherAllele, effectAllele, nonEffectAllele;
			double refAlleleFreq;
			while(mr.advanceLine() && rar.advanceLine() && tmp < testSize){
				EAFPairs[0][tmp] = Utils.fromInt(mr.getEAF(), MetaReader.EAF_WIDTH);
				refAllele = rar.getRefAllele();
				otherAllele = rar.getOtherAllele();
				effectAllele = mr.getEffectAllele();
				nonEffectAllele = mr.getNonEffectAllele();
				refAlleleFreq = rar.getRefAlleleFreq();
	 			if(refAlleleFreq < 0)
	 				EAFPairs[1][tmp] = null;
	 			else if(refAllele == effectAllele && otherAllele == nonEffectAllele)
	 				EAFPairs[1][tmp] = Utils.fromFixPoint(
							refAlleleFreq, 
							MetaReader.EAF_WIDTH, MetaReader.EAF_OFFSET);
				else if(refAllele == nonEffectAllele && otherAllele == effectAllele)
					EAFPairs[1][tmp] = Utils.fromFixPoint(
							1 - refAlleleFreq, 
							MetaReader.EAF_WIDTH, MetaReader.EAF_OFFSET);
				else
					EAFPairs[1][tmp] = null;
	 			tmp++;
			}
			mr.close();
			rar.close();
			
			logger.log(Level.INFO, "---------- Generator: End preparing input ----------");
		}

		@Override
		public void secureCompute(CompEnv<T> gen) throws Exception {
			logger.log(Level.INFO, "++++++++++ Generator: Computing P-Z value pairs ++++++++++");
			
			result = compute(gen, EAFPairs);
			
			logger.log(Level.INFO, "---------- Generator: End computing ----------");
		}

		@Override
		public void prepareOutput(CompEnv<T> gen) throws Exception {
			BufferedWriter bw = new BufferedWriter(new FileWriter("out/EAF.out"));
			for(int i = 0; i < result.length; i++){
				boolean[] plainEAFPair = gen.outputToAlice(result[i]);
				boolean[] eaf1Bools = new boolean[MetaReader.EAF_WIDTH];
				Arrays.fill(eaf1Bools, false);
				System.arraycopy(plainEAFPair, 0, eaf1Bools, MetaReader.EAF_WIDTH - EAF_preserved_bits, EAF_preserved_bits);
				boolean[] eaf2Bools = new boolean[MetaReader.EAF_WIDTH];
				Arrays.fill(eaf2Bools, false);
				System.arraycopy(plainEAFPair, EAF_preserved_bits, eaf2Bools, MetaReader.EAF_WIDTH - EAF_preserved_bits, EAF_preserved_bits);
				Double eaf1 = Utils.toFixPoint(eaf1Bools, MetaReader.EAF_OFFSET);
				Double eaf2 = Utils.toFixPoint(eaf2Bools, MetaReader.EAF_OFFSET);
				bw.write(eaf1 + "\t\t" + eaf2 + "\n");
			}
			bw.close();
		}
	}
	
	public static class Evaluator<T> extends EvaRunnable<T>{
		
		/** The study */
		String studyName;
		
		/** The reference*/
		String refName = "../data/reference/aligned_AlleleFreq_HapMap_CEU_phase3.2_nr.b36_fwd.txt";
		
		boolean[][][] EAFPairs;
		
		T[][] result;
		
		@Override
		public void prepareInput(CompEnv<T> gen) throws Exception {
			studyName = args[0];
			MetaReader mr = new Secure_EAF_Processor(new File(studyName));
			RefAFReader rar = new RefAFReader(new File(refName));
			
			logger.log(Level.INFO, "++++++++++ Generator: Preparing input from study file '"
					+ studyName
					+ "' ++++++++++");
			
			EAFPairs = new boolean[2][testSize][];
			int tmp = 0;
			char refAllele, otherAllele, effectAllele, nonEffectAllele;
			double refAlleleFreq;
			while(mr.advanceLine() && rar.advanceLine() && tmp < testSize){
				EAFPairs[0][tmp] = Utils.fromInt(mr.getEAF(), MetaReader.EAF_WIDTH);
				refAllele = rar.getRefAllele();
				otherAllele = rar.getOtherAllele();
				effectAllele = mr.getEffectAllele();
				nonEffectAllele = mr.getNonEffectAllele();
				refAlleleFreq = rar.getRefAlleleFreq();
	 			if(refAlleleFreq < 0)
	 				EAFPairs[1][tmp] = null;
	 			else if(refAllele == effectAllele && otherAllele == nonEffectAllele)
	 				EAFPairs[1][tmp] = Utils.fromFixPoint(
							refAlleleFreq, 
							MetaReader.EAF_WIDTH, MetaReader.EAF_OFFSET);
				else if(refAllele == nonEffectAllele && otherAllele == effectAllele)
					EAFPairs[1][tmp] = Utils.fromFixPoint(
							1 - refAlleleFreq, 
							MetaReader.EAF_WIDTH, MetaReader.EAF_OFFSET);
				else
					EAFPairs[1][tmp] = null;
	 			tmp++;
			}
			mr.close();
			rar.close();
			
			logger.log(Level.INFO, "---------- Evaluator: End preparing input ----------");
		}

		@Override
		public void secureCompute(CompEnv<T> gen) throws Exception {
			logger.log(Level.INFO, "++++++++++ Evaluator: Computing P-Z value pairs ++++++++++");
			
			result = compute(gen, EAFPairs);
			
			logger.log(Level.INFO, "---------- Evaluator: End computing ----------");
		}

		@Override
		public void prepareOutput(CompEnv<T> gen) throws Exception {
			for(int i = 0; i < result.length; i++){
				boolean[] eafPair = gen.outputToAlice(result[i]);
			}
		}
		
	}
}
