package ch.epfl.lca.genopri.secure.utils;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.HashMap;
import java.util.Scanner;
import java.util.logging.Level;

public class FileUtils{
	
	public static HashMap<String, String> getMapfromFile(String fileName){
		Scanner scanner = null;
		try {
			 scanner = new Scanner(new File(fileName));
		} catch (FileNotFoundException e) {
			Debugger.debug(Level.SEVERE, e.getMessage());
			System.exit(1);
		}
		HashMap<String, String>	map = new HashMap<String, String>();
		while(scanner.hasNextLine()){
			String[] pairs = scanner.nextLine().split("\\s+");
			map.put(pairs[0], pairs[1]);
		}
		scanner.close();
		return map;
	}
}
