package ch.epfl.lca.genopri.secure.utils;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.lang.reflect.Field;

import com.javamex.classmexer.MemoryUtil;

public class MemoryHeapMap {
	public static void dump(Object obj, File dumpFile) throws IllegalArgumentException, IllegalAccessException, IOException{
		BufferedWriter writer = new BufferedWriter(new FileWriter(dumpFile));
		Class<?> objClass = obj.getClass();
		Field[] fields = objClass.getFields();
		for(Field field : fields){
			String name = field.getName();
			Object value = field.get(obj);
			double size = 0;
			if(value != null)
				size = MemoryUtil.deepMemoryUsageOf(value) / 1000000.0;
			writer.write(name + ": " + String.valueOf(size) + "M\n");
		}
		double size = MemoryUtil.deepMemoryUsageOf(obj) / 1000000.0;
		writer.write("EAF_Processor.this: " + String.valueOf(size) + "M\n");
		writer.close();
	}
	
	public static void printGeneralMemInfo(){
		System.out.println("Max memory: " + Runtime.getRuntime().maxMemory() / 1000000 + "M");
		System.out.println("Total memory: " + Runtime.getRuntime().totalMemory() / 1000000 + "M");
		System.out.println("Free memory: " + Runtime.getRuntime().freeMemory() / 1000000 + "M");
		System.out.println("Used memory: " + (Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory()) / 1000000 + "M");
	}
}
