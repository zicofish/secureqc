package ch.epfl.lca.genopri.plain;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

import ch.epfl.lca.genopri.plain.utils.MedianFinder;


/**
 * @author zhihuang
 *
 */
public class SE_N_Processor extends MetaProcessor{
	private Logger logger = Logger.getLogger(SE_N_Processor.class.getName());
	
	/** The list of studies that are handled */
	List<String> studyList = new LinkedList<>();
	
	/** The maximum sample size for each study */
	List<Double> NmaxList = new LinkedList<>();
	
	/** The median standard error for each study */
	List<Double> medianSEList = new LinkedList<>();
	
	public SE_N_Processor(File dir){
		super(dir);
	}
	
	
	/**
	 * Process all files in the directory of studies, and generate the SE-N plot data
	 */
	@Override
	public void parseData() {
		for(File study : studiesDir.listFiles(new StudyFileFilter())){
			if(!processStudy(study))
				continue;
			logger.log(Level.INFO, "++++++++++ Start processing study file '"
					+ study.getName()
					+ "' ++++++++++");
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
	}


	/**
	 * Write out the SE-N plot data
	 */
	@Override
	public void write(File output) {
		BufferedWriter writer = null;
		try {
			 writer = new BufferedWriter(new FileWriter(output));
			 writer.write("Study\tNmax\tMedian(SE)\n");
			 for(int i = 0; i < studyList.size(); i++){
				 writer.write(studyList.get(i) + "\t"
				 		+ NmaxList.get(i) + "\t"
				 		+ medianSEList.get(i) + "\n");
			 }
			 writer.flush();
			 writer.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
