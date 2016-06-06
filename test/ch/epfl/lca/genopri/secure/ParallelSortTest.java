package ch.epfl.lca.genopri.secure;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;
import java.util.Random;

import ch.epfl.lca.genopri.secure.parallel.DataGraphNode;
import flexsc.CompEnv;
import flexsc.Party;
import gc.BadLabelException;
import graphsc.parallel.Gadget;
import graphsc.parallel.Machine;
import graphsc.parallel.SortGadget;
import util.Constants;
import util.Utils;

public class ParallelSortTest<T> extends Gadget<T>{

	public ParallelSortTest(CompEnv<T> env, Machine machine) {
		super(env, machine);
	}
	
	private boolean[][] getInput(int inputLength, int garblerId, int processors) throws IOException {
		System.out.println("inputLength: " + inputLength);
		int[] data = new int[inputLength];
		BufferedReader br = new BufferedReader(new FileReader(Constants.INPUT_DIR + "Sort" + inputLength * processors + ".in"));
		int j = 0;
		for (int i = 0; i < inputLength * processors; i++) {
			String readLine = br.readLine();
			if (!(i >= garblerId * inputLength && i < (garblerId + 1) * inputLength)) {
				continue;
			}
			data[j] = (Integer.parseInt(readLine));
			j++;
		}
		br.close();
		boolean[][] c = new boolean[data.length][];
		for(int i = 0; i < data.length; ++i) {
			c[i] = Utils.fromInt(data[i], 32);
		}
		return c;
	}

	@Override
	public Object secureCompute() throws Exception {
		long s = System.nanoTime();
		
		int inputLength = machine.getInputLength() / machine.getTotalMachines();
		boolean[][] data = null;
		if (env.getParty().equals(Party.Alice)) {
			data = new boolean[inputLength][32];
		} else {
			data = getInput(inputLength, machine.getGarblerId(), machine.getTotalMachines());;
		}
		T[][] tData = (T[][]) env.inputOfBob(data);
		DataGraphNode<T>[] nodes = new DataGraphNode[data.length];
		for (int i = 0; i < nodes.length; i++) {
			nodes[i] = new DataGraphNode<T>(null, null, null, tData[i], env);
		}
		
		new SortGadget<T>(env, machine)
		.setInputs(nodes, DataGraphNode.getDataComparator(env, 32))
		.secureCompute();
		
		print(machine.getGarblerId(), env, nodes);
		
		long e = System.nanoTime();
		System.out.println((env.getParty().equals(Party.Alice) ? "Garbler " : "Evaluator ") 
				+ machine.getGarblerId() + ": Sorting runtime " + (e-s)/1e9 + "s");
		return null;
	}

	private void print(int garblerId,
			final CompEnv<T> env,
			DataGraphNode<T>[] nodes) throws IOException, BadLabelException {
		BufferedWriter bw = null;
		if (Party.Alice.equals(env.getParty())) {
			 bw = new BufferedWriter(new FileWriter("out/secureSort" + machine.getInputLength() + ".out." + garblerId));
		}
		for (int i = 0; i < nodes.length; i++) {
			int u = Utils.toInt(env.outputToAlice(nodes[i].getData()));
			env.channel.flush();
			if (Party.Alice.equals(env.party)) {
				bw.write(u + "\n");
			}
	    }
		if(bw != null){
			bw.flush();
			bw.close();
		}
	}
	
	/*
	 * Just for generating a random array
	 */
	public static void main(String[] args) throws IOException{
		int arraySize = 4096;
		BufferedWriter bw = new BufferedWriter(new FileWriter("./run/in/Sort4096.in"));
		Random r = new Random();
		int[] array = new int[arraySize];
		for(int i = 0; i < arraySize; i++){
			array[i] = r.nextInt(30000);
			bw.write(array[i] + "\n");
		}
		bw.flush();
		bw.close();
		
		bw = new BufferedWriter(new FileWriter("./run/out/plainSort4096.out"));
		Arrays.sort(array);
		for(int i = 0; i < arraySize; i++)
			bw.write(array[i] + "\n");
		bw.flush();
		bw.close();
	}
}
