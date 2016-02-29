package ch.epfl.lca.genopri;
import java.io.File;
import java.io.FileFilter;
import java.util.regex.Pattern;


public class WomenFileFilter implements FileFilter{
	Pattern womenFile = Pattern.compile("*.WOMEN.*");

	@Override
	public boolean accept(File pathname) {
		return womenFile.matcher(pathname.getName()).matches();
	}
	
}