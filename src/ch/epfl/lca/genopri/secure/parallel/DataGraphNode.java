package ch.epfl.lca.genopri.secure.parallel;


import circuits.arithmetic.IntegerLib;
import flexsc.CompEnv;
import graphsc.parallel.GraphNode;
import graphsc.parallel.NodeComparator;

public class DataGraphNode<T> extends GraphNode<T>{
	
	private T[] data;
	
	public DataGraphNode(CompEnv<T> env, int dataLength){
		this(null, null, null, env.newTArray(dataLength), env);
	}
	
	public DataGraphNode(T[] data, CompEnv<T> env){
		this(null, null, null, data, env);
	}

	public DataGraphNode(T[] u, T[] v, T isVertex, T[] data, CompEnv<T> env) {
		super(u, v, isVertex);
		this.data = data;
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
	
	public void setData(T[] data){
		this.data = data;
	}
	
	public T[] getData() {
		return data;
	}
	
	public int getDataLength() {
		return data.length;
	}
}
