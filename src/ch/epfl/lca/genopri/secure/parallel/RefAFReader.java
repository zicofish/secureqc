package ch.epfl.lca.genopri.secure.parallel;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.HashMap;
import java.util.Scanner;
import java.util.logging.Level;

import ch.epfl.lca.genopri.secure.GenomicFileCheck;
import ch.epfl.lca.genopri.secure.utils.Debugger;

public class RefAFReader implements GenomicFileCheck{

	/** A reader for the current reference file */
	Scanner scanner = null;
	
	/** Variant map from rs# to [rs#, refallele, otherallele, refallele_freq] */
	HashMap<String, String[]> variantMap = null;
	
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
	
	HashMap<String, String[]> getVariantMap(){
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
}
