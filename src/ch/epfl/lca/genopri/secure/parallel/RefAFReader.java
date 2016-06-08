package ch.epfl.lca.genopri.secure.parallel;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Scanner;
import java.util.logging.Level;

import ch.epfl.lca.genopri.secure.GenomicFileCheck;
import ch.epfl.lca.genopri.secure.utils.Debugger;

public class RefAFReader implements GenomicFileCheck{

	/** A reader for the current reference file */
	Scanner scanner = null;
	
	/** Variant map from rs# to [rs#, refallele, otherallele, refallele_freq] */
	HashMap<String, String[]> variantMap = null;
	
	/** Varaint array of [rs#, refallele, otherallele, refallele_freq] */
	String[][] variantArray = null;
	
	/** A reference allele frequence file should organize their columns in this order */
	public final String[] expectedHeaders = new String[]{
		"rs#",
		"refallele",
		"otherallele",
		"refallele_freq"
	};
	
	RefAFReader(File file){
		try {
			scanner = new Scanner(file);
		} catch (FileNotFoundException e) {
			Debugger.debug(Level.SEVERE, "Cannot find the reference file '" + file + "'.");
			System.exit(1);
		}
		String[] headers = scanner.nextLine().split("\\s+");
		if(!matchHeaders(expectedHeaders, headers)){
			Debugger.debug(Level.SEVERE, "The headers of file '" + file + "' does not match the expected headers.");
			System.exit(1);
		}
	}
	
	
	/**
	 * This can consume much memory space. For example, when I load a reference file that is only 20MB with 1.4 million variants,
	 * it takes 400MB in memory to store the map. Might be able to optimized somewhere.
	 * @return A hash map from variant ID to [variant ID, reference allele, other allele, reference allele freqeuency]
	 */
	public HashMap<String, String[]> getVariantMap(){
		if(variantMap != null)
			return variantMap;
		variantMap = new HashMap<String, String[]>();
		while(scanner.hasNextLine()){
			String line = scanner.nextLine();
			String[] lineFields = line.split("\\s+");
			if(lineFields.length == 0) continue;	// SKIP empty lines
			if(lineFields.length != expectedHeaders.length){
				Debugger.debug(Level.WARNING, "The line '" + line + "' does not have expected number of fields.");
				continue;
			}
			variantMap.put(lineFields[0], lineFields);
		}
		scanner.close();
		return variantMap;
	}
	
	public String[][] getVariantArray(){
		if(variantArray != null)
			return variantArray;
		List<String[]> tmpList = new ArrayList<String[]>();
		while(scanner.hasNextLine()){
			String line = scanner.nextLine();
			String[] lineFields = line.split("\\s+");
			if(lineFields.length == 0) continue;	// SKIP empty lines
			if(lineFields.length != expectedHeaders.length){
				Debugger.debug(Level.WARNING, "The line '" + line + "' does not have expected number of fields.");
				continue;
			}
			tmpList.add(lineFields);
		}
		return Arrays.copyOf(tmpList.toArray(), tmpList.size(), String[][].class);
	}
}
