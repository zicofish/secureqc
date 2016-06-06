package ch.epfl.lca.genopri.secure;

public interface GenomicFileCheck {

	/**
	 * Check whether the headers match the expected headers in both number and order.
	 * @param headers
	 * @return true if matched, false otherwise.
	 */
	default public boolean matchHeaders(String[] expectedHeaders, String[] headers){
		if(expectedHeaders.length != headers.length) return false;
		for(int i = 0; i < expectedHeaders.length; i++)
			if(!expectedHeaders[i].equals(headers[i]))
				return false;
		return true;
	}
}
