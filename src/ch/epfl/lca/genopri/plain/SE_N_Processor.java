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
	
	/** The maximum sample size */
	private Double Nmax;
	
	/** The median standard error */
	private Double medianSE;
	
	public SE_N_Processor(File study){
		super(study);
	}
	
	@Override
	public void runProcessor() {
		logger.log(Level.INFO, "++++++++++ Start processing study file '"
				+ study.getName()
				+ "' ++++++++++");

		Nmax = 0.0;
		ArrayList<Double> standardErrors = new ArrayList<>(APPROX_SIZE);
		while(advanceLine()){
			Double tmpN = getN();
			if(Nmax < tmpN) Nmax = tmpN;
			standardErrors.add(getSE());
		}
		closeStudy();
		medianSE = MedianFinder.findMedian(standardErrors);
		
		logger.log(Level.INFO, "---------- End ----------");
	}

	public double getNmax(){
		return Nmax;
	}
	
	public double getMedianSE(){
		return medianSE;
	}
	
	@Override
	public String toString(){
		return "Nmax: " + Nmax + "\n"
				+ "Median SE: " + medianSE + "\n";
	}

//	/**
//	 * Write out the SE-N plot data
//	 */
//	@Override
//	public void write(File output) {
//		BufferedWriter writer = null;
//		try {
//			 writer = new BufferedWriter(new FileWriter(output));
//			 writer.write("Study\tNmax\tMedian(SE)\n");
//			 for(int i = 0; i < studyList.size(); i++){
//				 writer.write(studyList.get(i) + "\t"
//				 		+ NmaxList.get(i) + "\t"
//				 		+ medianSEList.get(i) + "\n");
//			 }
//			 writer.flush();
//			 writer.close();
//		} catch (IOException e) {
//			e.printStackTrace();
//		}
//	}
}
