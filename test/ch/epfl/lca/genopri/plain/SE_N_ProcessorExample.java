package ch.epfl.lca.genopri.plain;

import java.io.File;

public class SE_N_ProcessorExample {
	public static void main(String[] args){
//		File dir = new File("./data/zk_jfellay/GIANT_toy"),
//				output = new File("./data/output/SE_N_plot_data.txt");
		File dir = new File("./data/zk_jfellay/GIANT_toy/small"),
				output = new File("./data/output/small/SE_N_plot_data.small.txt");
		MetaProcessor processor = new SE_N_Processor(dir);
		processor.parseData();
		processor.write(output);
	}
	
}
