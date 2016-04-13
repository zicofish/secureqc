package ch.epfl.lca.genopri.secure;


import circuits.arithmetic.IntegerLib;
import flexsc.CompEnv;
import graphsc.parallel.GraphNode;
import graphsc.parallel.NodeComparator;
import util.Utils;

public class DataGraphNode<T> extends GraphNode<T>{

	static int DATA_LEN = 32; 
	
	T[] data;

	public DataGraphNode(T[] u, T[] v, T isVertex, T[] data, CompEnv<T> env) {
		super(u, v, isVertex);
		if(data.length != DATA_LEN)
			throw new IllegalArgumentException("data should be " + DATA_LEN + " bits.");
		this.data = data;
	}
	
	public DataGraphNode(CompEnv<T> env){
		super(env);
		this.data = env.newTArray(DATA_LEN);
	}

	@Override
	public T[] flatten(CompEnv<T> env) {
//		T[] vert = env.newTArray(1);
//		vert[0] = (T) isVertex;
//		return Utils.flatten(env, u, v, vert, data);
		return data;
	}

	@Override
	public void unflatten(T[] flat, CompEnv<T> env) {
//		T[] vert = env.newTArray(1);
//		Utils.unflatten(flat, u, v, vert, data);
//		isVertex = vert[0];
		data = flat;
	}
	
	public static <T> NodeComparator<T> getDataComparator(final CompEnv<T> env, final int dataLength) {
		IntegerLib<T> lib = new IntegerLib<T>(env, dataLength);
		NodeComparator<T> dataComparator = new NodeComparator<T>() {

			@Override
			public T leq(GraphNode<T> n1, GraphNode<T> n2) {
				return lib.leq(((DataGraphNode<T>)n1).data, ((DataGraphNode<T>)n2).data);
			}
		};
		return dataComparator;
	}
}
