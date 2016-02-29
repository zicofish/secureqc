package ch.epfl.lca.genopri;
import java.io.File;
import java.io.FileFilter;
import java.util.regex.Pattern;


public class MenFileFilter implements FileFilter{
	Pattern menFile = Pattern.compile("*.MEN.*");
	@Override
		public boolean accept(File pathname) {
		return menFile.matcher(pathname.getName()).matches();
	}
}