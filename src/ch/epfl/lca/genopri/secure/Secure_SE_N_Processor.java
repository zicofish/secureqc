package ch.epfl.lca.genopri.secure;

import java.io.File;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.logging.Level;
import java.util.logging.Logger;

import ch.epfl.lca.genopri.plain.utils.MedianFinder;

import com.oblivm.backend.flexsc.CompEnv;
import com.oblivm.backend.util.GenRunnable;

public class Secure_SE_N_Processor extends SecureMetaProcessor{
	private static Logger logger = Logger.getLogger(Secure_SE_N_Processor.class.getName());
	
	protected Secure_SE_N_Processor(File study) {
		super(study);
	}

	public static class Generator<T> extends GenRunnable<T>{

		@Override
		public void prepareInput(CompEnv<T> gen) throws Exception {
			File studyList = new File(args[0]);
			Scanner scanner = new Scanner(studyList);
			while(scanner.hasNextLine()){
				String studyName = scanner.nextLine();
				SecureMetaProcessor smp = new Secure_SE_N_Processor(new File(studyName));
				logger.log(Level.INFO, "++++++++++ Start processing study file '"
						+ studyName
						+ "' ++++++++++");
			}
			for(File study : studiesDir.listFiles(new StudyFileFilter())){
				if(!processStudy(study))
					continue;
				
				studyList.add(study.getName());
				Double Nmax = 0.0;
				ArrayList<Double> standardErrors = new ArrayList<>(APPROX_SIZE);
				while(advanceLine()){
					Double tmpN = getN();
					if(Nmax < tmpN) Nmax = tmpN;
					standardErrors.add(getSE());
				}
				closeStudy();
				NmaxList.add(Nmax);
				double medianSE = MedianFinder.findMedian(standardErrors);
				medianSEList.add(medianSE);
				
				logger.log(Level.INFO, "---------- End ----------");
			}
			
			logger.log(Level.INFO, "========== End processing the whole directory ==========");
			SecureMetaProcessor smp = new Secure_SE_N_Processor();
			
		}

		@Override
		public void secureCompute(CompEnv<T> gen) throws Exception {
			// TODO Auto-generated method stub
			 
		}

		@Override
		public void prepareOutput(CompEnv<T> gen) throws Exception {
			// TODO Auto-generated method stub
			
		}
		
	}
}
