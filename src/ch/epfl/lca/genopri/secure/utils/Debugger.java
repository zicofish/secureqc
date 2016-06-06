package ch.epfl.lca.genopri.secure.utils;

import java.util.logging.Level;
import java.util.logging.Logger;

import flexsc.CompEnv;
import flexsc.Party;

public class Debugger {
	public static final Logger logger = Logger.getLogger(Debugger.class.getName());
	
	public static void setOutputLevel(Level level){
		logger.setLevel(level);
	}
	
	public static <T> void debug(int garblerId, CompEnv<T> env, String message){
		logger.log(Level.INFO, "============== "
				+ (env.getParty().equals(Party.Alice) ? "Generator " : "Evaluator ")
				+ garblerId + " :" + message + " ==============");
	}
	
	public static void debug(Level level, String message){
		logger.log(level, message);
	}
}
