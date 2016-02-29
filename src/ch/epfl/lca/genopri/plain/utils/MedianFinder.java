package ch.epfl.lca.genopri.plain.utils;

import java.util.ArrayList;
import java.util.Random;

/**
 * @author zhihuang
 *
 */
public class MedianFinder {
	public static <T extends Comparable<T>> T findMedian(ArrayList<T> array){
		return findKthElement(array, 0, array.size() - 1, array.size() / 2);
	}
	
	private static <T extends Comparable<T>> T findKthElement(ArrayList<T> array, int start, int end, int k){
		if(start == end)
			return array.get(start);
		int partitionPoint = partition(array, start, end);
		if(partitionPoint - start == k)
			return array.get(partitionPoint);
		else if(partitionPoint - start < k)
			return findKthElement(array, partitionPoint + 1, end, k - (partitionPoint - start + 1));
		else
			return findKthElement(array, start, partitionPoint - 1, k);
	}
	
	private static <T extends Comparable<T>> int partition(ArrayList<T> array, int start, int end){
		int randomDraw = start + new Random().nextInt(end - start + 1);
		T tmp = array.get(randomDraw);
		array.set(randomDraw, array.get(start));
		int left = start, right = end;
		while(left < right){
			while(left < right && array.get(right).compareTo(tmp) > 0) right--;
			if(left < right){
				array.set(left, array.get(right));
				left++;
			}
			while(left < right && array.get(left).compareTo(tmp) < 0) left++;
			if(left < right){
				array.set(right, array.get(left));
				right--;
			}
		}
		array.set(left, tmp);
		return left;
	}
}
