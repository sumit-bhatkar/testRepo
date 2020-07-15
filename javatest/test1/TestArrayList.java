package javatest.test1;

import java.util.*; 


public class TestArrayList {
	
	public static void main (String args[]) {
		ArrayList<String> al=new ArrayList<String>();  
		al.add("zRavi");  
		al.add("Vijay");  
		al.add("Ajay");  
 
		Iterator itr=al.iterator();  
		
		while(itr.hasNext()){  
			System.out.println(itr.next());  
		}
//		System.out.println("========================");  
//		for (String s:al) {
//			System.out.println(s);  
//		}
//		
		Collections.sort(al);
		
//		System.out.println("=============Sorted while==========="); 
//		Iterator itr2=al.iterator();
//		while(itr2.hasNext()){  
//			System.out.println(itr2.next());  
//		}
		
		System.out.println("=============Sorted For===========");  

		for (int i = 0;i <al.size();i++) {
			System.out.println("item - " + i + "  " + al.get(i));  
		}
		
//		for (String s:al) {
//			System.out.println(s);  
//		}
		
		System.out.println("=============Sorted For===========");  
		String eventData_calleeValue = "VijaySaravanana";
		
		for (String prefix : al) {
			if (prefix.equals(eventData_calleeValue.substring(0, prefix.length()))){
				System.out.println("Matched with " + prefix); 
			}
			else 
			{
				System.out.println("Not Matched with " + prefix);
			}
		}
		
		
	}

}
