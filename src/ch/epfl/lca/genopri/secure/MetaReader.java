package ch.epfl.lca.genopri.secure;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.logging.Level;

import ch.epfl.lca.genopri.secure.utils.Base64Utils;
import ch.epfl.lca.genopri.secure.utils.Debugger;

/**
 * @author zhihuang
 *
 */
public class MetaReader implements GenomicFileCheck{
	
	/** bit length for fix-point representation of a standard error */
	public static final int SE_WIDTH = 32;
	public static final int SE_OFFSET = 24;
	
	/** bit length for fix-point representation of a beta estimate */
	public static final int BETA_WIDTH = 32;
	public static final int BETA_OFFSET = 24;
	
	/** bit length for fix-point representation of a p value */
	public static final int P_WIDTH = 64;
	public static final int P_OFFSET = 62;
	
	/** bit length for fix-point representation of a eaf value */
	public static final int EAF_WIDTH = 32;
	public static final int EAF_OFFSET = 30;
	
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
	
	public MetaReader(File study){
		try {
			studyScanner = new Scanner(study);
		} catch (FileNotFoundException e) {
			Debugger.debug(Level.SEVERE, "Cannot find the study file '" + study + "'.");
			System.exit(1);
		}
		String[] headers = studyScanner.nextLine().split("\\s+");
		if(!matchHeaders(expectedHeaders, headers)){
			Debugger.debug(Level.SEVERE, "The headers of study '" + study + "' does not match the expected headers.");
			System.exit(1);
		}
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
				Debugger.debug(Level.WARNING, "The line '" + line + "' does not have expected number of fields.");
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
	 * Marker name
	 */
	public String getMarker(){
		return lineFields[0];
	}
	
	/**
	 * Effect allele
	 */
	public String getEffectAllele(){
		return lineFields[3];
	}
	
	/**
	 * Non-effect allele
	 */
	public String getNonEffectAllele(){
		return lineFields[4];
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
