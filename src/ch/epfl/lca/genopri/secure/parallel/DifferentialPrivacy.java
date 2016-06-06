package ch.epfl.lca.genopri.secure.parallel;

import org.apache.commons.math3.distribution.LaplaceDistribution;
import org.apache.commons.math3.distribution.NormalDistribution;

public class DifferentialPrivacy {
	private double sensitivity, epsilon, delta;
	
	public DifferentialPrivacy(double sensitivity, double epsilon, double delta){
		this.sensitivity = sensitivity;
		this.epsilon = epsilon;
		this.delta = delta;
	}
	
	public double[] genNoises(int size, String method){
		if(method.equals("gaussian")){
			double c = Math.sqrt(2 * Math.log(1.25 / this.delta));
		    double std = c * this.sensitivity / this.epsilon;
			NormalDistribution nd = new NormalDistribution(0, std);
			return nd.sample(size);
		}
		else if(method.equals("laplacian")){
			double scale = this.sensitivity / this.epsilon;
			LaplaceDistribution ld = new LaplaceDistribution(0, scale);
			return ld.sample(size);
		}
		return null;
	}
}
