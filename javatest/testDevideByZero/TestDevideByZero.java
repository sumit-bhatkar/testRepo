package javatest.testDevideByZero;

public class TestDevideByZero {

	public static void main(String[] args) {
		double a=0,	b=0;
		int kpiValue = 5;
//		double kpiValue = 5;
		int thr = 97;

		kpiValue = ((int) (a/(double) b));
		//kpiValue = ( (a/(double) b));   //When kept double it is NaN 
		System.out.println ("value " +kpiValue );

		if (thr > 0 && kpiValue > thr)
			System.out.println ("True");
		else
			System.out.println ("False");

		if (kpiValue < thr)
			System.out.println ("True");
		else
			System.out.println ("False");

	}

}
