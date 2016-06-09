package ch.epfl.lca.genopri.secure.utils;

import java.io.File;
import java.io.IOException;
import java.util.logging.ConsoleHandler;
import java.util.logging.FileHandler;
import java.util.logging.Formatter;
import java.util.logging.Level;
import java.util.logging.LogRecord;
import java.util.logging.Logger;

import flexsc.CompEnv;
import flexsc.Party;

public class Debugger {
	public static final Logger logger = Logger.getLogger(Debugger.class.getName());
	
	static
	{
		ConsoleHandler handler = new ConsoleHandler();
		handler.setFormatter(new BriefFormatter());
		logger.addHandler(handler);
	}
	
	public static void setLogFile(String fileName) throws SecurityException, IOException{
		FileHandler handler = new FileHandler(fileName);
		handler.setFormatter(new BriefFormatter());
		logger.addHandler(handler);
	}
	
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
	
	static class BriefFormatter extends Formatter{

		@Override
		public String format(LogRecord record) {
			return record.getMessage() + "\n";
		}
		
	}
}
