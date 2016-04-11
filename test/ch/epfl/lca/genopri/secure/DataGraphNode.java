package ch.epfl.lca.genopri.secure;


import circuits.arithmetic.IntegerLib;
import flexsc.CompEnv;
import parallel.GraphNode;
import parallel.NodeComparator;
import util.Utils;

public class DataGraphNode<T> extends GraphNode<T>{

	T[] data;
	IntegerLib<T> lib;

	public DataGraphNode(T[] u, T[] v, T isVertex, T[] data, CompEnv<T> env) {
		super(u, v, isVertex);
		this.data = data;
		lib = new IntegerLib<T>(env, data.length);
	}

	@Override
	public T[] flatten(CompEnv<T> env) {
		T[] vert = env.newTArray(1);
		vert[0] = (T) isVertex;
		return Utils.flatten(env, u, v, vert, data);
	}

	@Override
	public void unflatten(T[] flat, CompEnv<T> env) {
		T[] vert = env.newTArray(1);
		Utils.unflatten(flat, u, v, vert, data);
		isVertex = vert[0];
	}
	
	public NodeComparator<T> getDataComparator(final CompEnv<T> env) {
		NodeComparator<T> dataComparator = new NodeComparator<T>() {

			@Override
			public T leq(GraphNode<T> n1, GraphNode<T> n2) {
				return lib.leq(((DataGraphNode<T>)n1).data, ((DataGraphNode<T>)n2).data);
			}
		};
		return dataComparator;
	}
}
