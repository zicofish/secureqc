package ch.epfl.lca.genopri.secure.parallel;

import java.io.File;
import java.io.IOException;

import com.javamex.classmexer.MemoryUtil;

import ch.epfl.lca.genopri.secure.utils.MemoryHeapMap;

public class RefAFReaderTest {
	public static void main(String[] main) throws IOException{
		long s = System.currentTimeMillis();
		RefAFReader rar = new RefAFReader(new File("./data/reference/aligned_AlleleFreq_HapMap_CEU_phase3.2_nr.b36_fwd.txt"));
		while(rar.advanceLine());
		
		MemoryHeapMap.printGeneralMemInfo();
//		System.out.println("varArray: " + MemoryUtil.deepMemoryUsageOf(varArray) / 1000000.0 + "Mbytes");
//		System.out.println("varArray[2]: " + MemoryUtil.deepMemoryUsageOf(varArray[2]) + "bytes");
//		System.out.println("varArray[2][0]: " + MemoryUtil.deepMemoryUsageOf(varArray[2][0]) + "bytes");
//		System.out.println("varArray[2][1]: " + MemoryUtil.deepMemoryUsageOf(varArray[2][1]) + "bytes");
//		System.out.println("varArray[2][2]: " + MemoryUtil.deepMemoryUsageOf(varArray[2][2]) + "bytes");
		
		long e = System.currentTimeMillis();
		System.out.println("Timing: " + (e - s) / 1000.0 + "s");
	}
}
