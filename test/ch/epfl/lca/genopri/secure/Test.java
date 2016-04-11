package ch.epfl.lca.genopri.secure;

import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.security.Security;

import rand.ISAACProvider;

public class Test {
	static SecureRandom rnd = null;
	static{
		Security.addProvider(new ISAACProvider());
		try {
			rnd = SecureRandom.getInstance("ISAACRandom");
	
		} catch (NoSuchAlgorithmException e) {
			e.printStackTrace();
			System.exit(1);
		}
	}
	public static void main(String[] args){
		
		System.out.println(rnd.nextLong());
	}
}
