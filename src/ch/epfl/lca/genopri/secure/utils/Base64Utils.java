package ch.epfl.lca.genopri.secure.utils;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.logging.Level;
import java.util.logging.Logger;

import org.bouncycastle.util.encoders.Base64;

public class Base64Utils {
	private static Logger logger = Logger.getLogger(Base64Utils.class.getName());
	
	public static int fromBase64ToInt(String str){
		byte[] intBytes = Base64.decode(str);
		if(intBytes.length != 4){
			logger.log(Level.SEVERE, "The base64 string does not decode to 4 bytes.");
			throw new RuntimeException();
		}
		ByteBuffer buf = ByteBuffer.wrap(intBytes);
		buf.order(ByteOrder.LITTLE_ENDIAN);
		return buf.getInt();
	}
	
	public static long fromBase64ToLong(String str){
		byte[] longBytes = Base64.decode(str);
		if(longBytes.length != 8){
			logger.log(Level.SEVERE, "The base64 string does not decode to 8 bytes.");
			throw new RuntimeException();
		}
		ByteBuffer buf = ByteBuffer.wrap(longBytes);
		buf.order(ByteOrder.LITTLE_ENDIAN);
		return buf.getLong();
	}
}
