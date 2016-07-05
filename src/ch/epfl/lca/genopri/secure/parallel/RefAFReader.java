package ch.epfl.lca.genopri.secure.parallel;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.logging.Level;

import ch.epfl.lca.genopri.secure.GenomicFileCheck;
import ch.epfl.lca.genopri.secure.utils.Debugger;

public class RefAFReader implements GenomicFileCheck{

	/** A reader for the current reference file */
//	Scanner scanner = null;  // Scanner is slower and uses more memory (during processing) than BufferedReader
	BufferedReader br = null;
	
	/** Variant map from rs# to [rs#, refallele, otherallele, refallele_freq] */
	HashMap<String, String[]> variantMap = null;
	
	/** Varaint array of [rs#, refallele, otherallele, refallele_freq] */
	Object[][] variantArray = null;
	
	/** A reference allele frequence file should organize their columns in this order */
	public final String[] expectedHeaders = new String[]{
		"rs#",
		"refallele",
		"otherallele",
		"refallele_freq"
	};
	
	/** The current row separated into the corresponding columns */
	private String[] lineFields = null;
	
	public RefAFReader(File file) throws IOException{
		try {
			br = new BufferedReader(new FileReader(file));
		} catch (FileNotFoundException e) {
			Debugger.debug(Level.SEVERE, "Cannot find the reference file '" + file + "'.");
			System.exit(1);
		}
		String[] headers = br.readLine().split("\\s+");
		if(!matchHeaders(expectedHeaders, headers)){
			Debugger.debug(Level.SEVERE, "The headers of file '" + file + "' does not match the expected headers.");
			System.exit(1);
		}
	}
	
	
	/**
	 * This can consume much memory space. For example, when I load a reference file that is only 20MB with 1.4 million variants,
	 * it takes 400MB in memory to store the map. Might be able to optimized somewhere.
	 * @return A hash map from variant ID to [variant ID, reference allele, other allele, reference allele freqeuency]
	 * @throws IOException 
	 */
	public HashMap<String, String[]> getVariantMap() throws IOException{
		if(variantMap != null)
			return variantMap;
		variantMap = new HashMap<String, String[]>();
		while(true){
			String line = br.readLine();
			if(line == null)
				break;
			String[] lineFields = line.split("\\s+");
			if(lineFields.length == 0) continue;	// SKIP empty lines
			if(lineFields.length != expectedHeaders.length){
				Debugger.debug(Level.WARNING, "The line '" + line + "' does not have expected number of fields.");
				continue;
			}
			variantMap.put(lineFields[0], lineFields);
		}
		br.close();
		return variantMap;
	}
	
	/**
	 * Assuming the reference file has the same list of variants in the same order as the study file, otherwise it takes too
	 * much memory to store the variant array.
	 * @throws IOException 
	 */
	public Object[][] getVariantArray(int size) throws IOException{
		if(variantArray != null)
			return variantArray;
//		List<String[]> tmpList = new ArrayList<String[]>();
//		variantArray = new Object[size][3];  // This representation uses more memory because of data alignment issue
		variantArray = new Object[3][size];
		int i = 0;
		while(i < size){
			String line = br.readLine();
			if(line == null)
				break;
			lineFields = line.split("\\s+");
			if(lineFields.length == 0) continue;	// SKIP empty lines
			if(lineFields.length != expectedHeaders.length){
				Debugger.debug(Level.WARNING, "The line '" + line + "' does not have expected number of fields.");
				continue;
			}
			variantArray[0][i] = new Character(lineFields[1].charAt(0));
			variantArray[1][i] = new Character(lineFields[2].charAt(0));
			variantArray[2][i] = Double.valueOf(lineFields[3]);
			i++;
		}
		br.close();
		return variantArray;
//		return Arrays.copyOf(tmpList.toArray(), tmpList.size(), String[][].class);
	}
	
	/** 
	 * Read the next valid row. A row is valid if and only if it has expected number of fields.
	 * @return true if there is a valid row to be read.
	 * @throws IOException 
	 */
	public boolean advanceLine() throws IOException{
		while(true){
			String line = br.readLine();
			if(line == null)
				break;
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
	
	public void close() throws IOException{
		br.close();
	}
	
	public char getRefAllele(){
		return lineFields[1].charAt(0);
	}
	
	public char getOtherAllele(){
		return lineFields[2].charAt(0);
	}
	
	public double getRefAlleleFreq(){
		return Double.valueOf(lineFields[3]);
	}
	
}
