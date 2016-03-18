package ch.epfl.lca.genopri.plain;

import java.io.File;


public class P_Z_ProcessorExample {
	public static void main(String[] args){
		File study = new File("./data/zk_jfellay/GIANT_toy/small/CLEAN.AGES.HEIGHT.MEN.GT50.20100914.small.txt");
		MetaProcessor processor = new P_Z_Processor(study);
		processor.runProcessor();
//		System.out.println(processor);
		
		System.out.println(((P_Z_Processor)processor).toSortedString());
	}
}
