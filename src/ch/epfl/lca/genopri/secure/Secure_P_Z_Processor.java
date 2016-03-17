package ch.epfl.lca.genopri.secure;

import java.io.File;
import java.util.ArrayList;
import java.util.logging.Level;
import java.util.logging.Logger;

import com.oblivm.backend.flexsc.CompEnv;
import com.oblivm.backend.util.EvaRunnable;
import com.oblivm.backend.util.GenRunnable;
import com.oblivm.backend.util.Utils;

public class Secure_P_Z_Processor extends SecureMetaProcessor{
	private static Logger logger = Logger.getLogger(Secure_P_Z_Processor.class.getName());
	
	protected Secure_P_Z_Processor(File study) {
		super(study);
	}

	public static class Generator<T> extends GenRunnable<T>{
		
		/** The study */
		String studyName;
		
		/** The reported P values */
		T[][] pValues;
		
		/** The Z-statistics based on reported beta estimate and standard error */
		T[][] zStats;
		
		/** Generator's input (list of p-value shares) */
		T[][] inputA;
		
		/** Evaluator's input. Because this class is a Generator, inputB will contain random elements. */
		T[][] inputB;
		
		@Override
		public void prepareInput(CompEnv<T> gen) throws Exception {
			studyName = args[0];
			SecureMetaProcessor smp = new Secure_SE_N_Processor(new File(studyName));
			logger.log(Level.INFO, "++++++++++ Generator: Preparing input from study file '"
					+ studyName
					+ "' ++++++++++");
			
			Nmax = 0.0;
			ArrayList<Integer> standardErrors = new ArrayList<>(APPROX_SIZE);
			while(smp.advanceLine()){
				Double tmpN = smp.getN();
				if(Nmax < tmpN) Nmax = tmpN;
				standardErrors.add(smp.getSE());
			}
			smp.closeStudy();
			boolean[][] temp = new boolean[standardErrors.size()][];
			for(int i = 0; i < standardErrors.size(); i++)
				temp[i] = Utils.fromInt(standardErrors.get(i), SE_BIT_LEN);
			
			inputA = gen.inputOfAlice(temp);
			inputB = gen.inputOfBob(new boolean[temp.length][SE_BIT_LEN]);
			
			logger.log(Level.INFO, "---------- Generator: End preparing input ----------");
		}

		@Override
		public void secureCompute(CompEnv<T> gen) throws Exception {
			logger.log(Level.INFO, "++++++++++ Generator: Computing median standar error ++++++++++");
			
			medianSE = compute(gen, inputA, inputB);
			
			logger.log(Level.INFO, "---------- Generator: End computing ----------");
		}

		@Override
		public void prepareOutput(CompEnv<T> gen) throws Exception {
			boolean[] plainMedian = gen.outputToAlice(medianSE);
			logger.log(Level.INFO, "========== Generator: median SE is " + Utils.toFixPoint(plainMedian, 24) + " ==========");
		}
	}
	
	public static class Evaluator<T> extends EvaRunnable<T>{
		
		/** The study */
		String studyName;
		
		/** The maximum sample size of the study */
		Double Nmax;
		
		/** The median standard error of the study */
		T[] medianSE;
		
		/** Generator's input  */
		T[][] inputA;
		
		/** Evaluator's input (list of SE shares). */
		T[][] inputB;
		
		@Override
		public void prepareInput(CompEnv<T> gen) throws Exception {
			studyName = args[0];
			SecureMetaProcessor smp = new Secure_SE_N_Processor(new File(studyName));
			logger.log(Level.INFO, "++++++++++ Evaluator: Preparing input from study file '"
					+ studyName
					+ "' ++++++++++");
			
			Nmax = 0.0;
			ArrayList<Integer> standardErrors = new ArrayList<>(APPROX_SIZE);
			while(smp.advanceLine()){
				Double tmpN = smp.getN();
				if(Nmax < tmpN) Nmax = tmpN;
				standardErrors.add(smp.getSE());
			}
			smp.closeStudy();
			boolean[][] temp = new boolean[standardErrors.size()][];
			for(int i = 0; i < standardErrors.size(); i++)
				temp[i] = Utils.fromInt(standardErrors.get(i), SE_BIT_LEN);

			inputA = gen.inputOfAlice(new boolean[temp.length][SE_BIT_LEN]);
			inputB = gen.inputOfBob(temp);
			
			logger.log(Level.INFO, "---------- Evaluator: End preparing input ----------");
		}

		@Override
		public void secureCompute(CompEnv<T> gen) throws Exception {
			logger.log(Level.INFO, "++++++++++ Evaluator: Computing median standar error ++++++++++");
			
			medianSE = compute(gen, inputA, inputB);
			
			logger.log(Level.INFO, "---------- Evaluator: End computing ----------");
		}

		@Override
		public void prepareOutput(CompEnv<T> gen) throws Exception {
			gen.outputToAlice(medianSE);
		}
		
	}
}
