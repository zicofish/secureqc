package ch.epfl.lca.genopri.secure;

import java.io.File;
import java.io.FileFilter;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.logging.Level;
import java.util.logging.Logger;

import ch.epfl.lca.genopri.secure.utils.Base64Utils;

/**
 * @author zhihuang
 *
 */
public abstract class SecureMetaProcessor {
	private Logger logger = Logger.getLogger(SecureMetaProcessor.class.getName());
	
	/** bit length for fix-point representation of a standard error */
	protected static final int SE_WIDTH = 32;
	protected static final int SE_OFFSET = 24;
	
	/** bit length for fix-point representation of a beta estimate */
	protected static final int BETA_WIDTH = 32;
	protected static final int BETA_OFFSET = 24;
	
	/** bit length for fix-point representation of a p value */
	protected static final int P_WIDTH = 64;
	protected static final int P_OFFSET = 62;
	
	/** Approximate number of SNPs in a study file. It is just used for initialization of a java list. */
	public static final int APPROX_SIZE = 3000000;
	
	/** A study file should organize their columns in this order */
	public static final String[] expectedHeaders = new String[]{
		"MarkerName",
		"Strand",
		"N",
		"Effect_allele",
		"Other_allele",
		"EAF",
		"Imputation",
		"Information_type",
		"Information",
		"BETA",
		"SE",
		"P",
		"MAC"
	};
	
	/** A reader for the current study file */
	private Scanner studyScanner = null;
	
	/** The current row separated into the corresponding columns */
	private String[] lineFields = null;
	
	protected SecureMetaProcessor(File study){
		try {
			studyScanner = new Scanner(study);
		} catch (FileNotFoundException e) {
			logger.log(Level.WARNING, "Cannot find the study file '" + study + "'.");
			System.exit(1);
		}
		String[] headers = studyScanner.nextLine().split("\\s+");
		if(!matchHeaders(headers)){
			logger.log(Level.WARNING, "The headers of study '" + study + "' does not match the expected headers.");
			System.exit(1);
		}
	}
	
	
	/**
	 * Check whether the headers match the expected headers in both number and order.
	 * @param headers
	 * @return true if matched, false otherwise.
	 */
	public boolean matchHeaders(String[] headers){
		if(expectedHeaders.length != headers.length) return false;
		for(int i = 0; i < expectedHeaders.length; i++)
			if(!expectedHeaders[i].equals(headers[i]))
				return false;
		return true;
	}
	
	
	/** 
	 * Read the next valid row. A row is valid if and only if it has expected number of fields.
	 * @return true if there is a valid row to be read.
	 */
	public boolean advanceLine(){
		while(studyScanner.hasNextLine()){
			String line = studyScanner.nextLine();
			lineFields = line.split("\\s+");
			if(lineFields.length == 0) continue;	// SKIP empty lines
			if(lineFields.length != expectedHeaders.length){
				logger.log(Level.WARNING, "The line '" + line + "' does not have expected number of fields.");
				continue;
			}
			return true;
		}
		return false;
	}
	
	/**
	 * Close the study
	 */
	public void closeStudy(){
		studyScanner.close();
	}
	
	
	/**
	 * The number of subjects analyzed for the current SNP (the current row)
	 */
	public double getN(){
		return Double.valueOf(lineFields[2]);
	}
	
	/**
	 * The effect allele frequency (range 0-1) for the current SNP (the current row)
	 */
	public int getEAF(){
		return Base64Utils.fromBase64ToInt(lineFields[5]);
	}
	
	/**
	 * Beta estimate (effect size) for the current SNP (the current row)
	 */
	public int getBETA(){
		return Base64Utils.fromBase64ToInt(lineFields[9]);
	}
	
	/**
	 * Estimated standard error on the estimate of the effect size for the current SNP (the current row)
	 */
	public int getSE(){
		return Base64Utils.fromBase64ToInt(lineFields[10]);
	}
	
	/**
	 * Significance of the variant association for the current SNP (the current row)
	 */
	public Long getP(){
		return Base64Utils.fromBase64ToLong(lineFields[11]);
	}
}
