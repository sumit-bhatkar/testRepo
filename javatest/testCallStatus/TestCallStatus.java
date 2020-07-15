package javatest.testCallStatus;

public class TestCallStatus {

	public static void main(String[] args) {
		System.out.println("========== START ==============");  
		int callStatus = 22; //31
		
		int iamPresent = (callStatus & 0x01);
		int acmPresent = ((callStatus & 0x02) >> 1 );
		int anmPresent = ((callStatus & 0x04) >> 2) ;
		int relPresent = ((callStatus & 0x08) >> 3 );
		int rlcPresent = ((callStatus & 0x10) >> 4 );
		System.out.println("iamPresent = " + iamPresent);
		System.out.println("acmPresent = " + acmPresent); 
		System.out.println("anmPresent = " + anmPresent); 
		System.out.println("relPresent = " + relPresent); 
		System.out.println("rlcPresent = " + rlcPresent); 

 		
			
		System.out.println("==========  END  ==============");   

	}
}
