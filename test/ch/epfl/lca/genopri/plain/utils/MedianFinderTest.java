package ch.epfl.lca.genopri.plain.utils;

import static org.junit.Assert.*;

import java.util.ArrayList;
import java.util.Arrays;

import org.junit.Test;

public class MedianFinderTest {

	@Test
	public void testFindMedian() {
		Double[] d = new Double[]{1.2, 3.4, 2.3};
		ArrayList<Double> array = new ArrayList<>();
		array.addAll(Arrays.asList(d));
		assertEquals((Double)2.3, MedianFinder.findMedian(array));
		
		array.remove(2.3);
		assertEquals((Double)3.4, MedianFinder.findMedian(array));
		
		array.remove(1.2);
		assertEquals((Double)3.4, MedianFinder.findMedian(array));
	}

}
