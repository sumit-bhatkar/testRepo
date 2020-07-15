package javatest.testServiceId;

import java.util.ArrayList;

public class TestServiceId {

	static class  ServiceIdData{
		public long fromGT = 0;
		public long toGT = 0;
		public int ssn = 0;
		public int tt = 0;
		public int serviceId = 0;
		
		ServiceIdData(long fgt, long tgt, int i_ssn, int i_tt, int i_serviceId){
			fromGT = fgt;
			toGT = tgt;
			ssn = i_ssn;
			tt = i_tt;
			serviceId = i_serviceId;
		}
	}
	
	public static ArrayList <ServiceIdData> serviceIdCache;
	
	public static void main(String[] args) {
		System.out.println("========== START ==============");
		serviceIdCache = new ArrayList <ServiceIdData>();
		initializeServiceIdCache();
		
		System.out.println("Test 1  [" + (getServiceId(123456789000010L,101,11) == 1)+ "]");
		System.out.println("Test 2  [" + (getServiceId(1111111111111112L,102,22) == 2)+ "]");
		System.out.println("Test 3  [" + (getServiceId(123456789000011L,0,33) == 3)+ "]");
		System.out.println("Test 4  [" + (getServiceId(123456789000012L,103,0) == 4)+ "]");
		System.out.println("Test 5  [" + (getServiceId(0,104,0) == 5)+ "]");
		System.out.println("Test 6  [" + (getServiceId(0,0,44) == 6)+ "]");
		
		System.out.println("Test 7  [" + (getServiceId(0,1,0) == 0)+ "]");
		System.out.println("Test 8  [" + (getServiceId(0,0,1) == 0)+ "]");
		System.out.println("Test 9  [" + (getServiceId(1,0,0) == 0)+ "]");
		System.out.println("Test 10 [" + (getServiceId(1111111111111110L,102,22) == 0)+ "]");
		System.out.println("Test 11 [" + (getServiceId(1111111111112000L,102,22) == 0)+ "]");
		System.out.println("Test 12 [" + (getServiceId(1111111111111111L,102,22) == 2)+ "]");
		System.out.println("Test 13 [" + (getServiceId(1111111111111999L,112,22) == 0)+ "]");
		System.out.println("Test 14 [" + (getServiceId(1111111111111999L,102,23) == 0)+ "]");

		
		System.out.println("=========== END ===============");
	}
	
	public static void initializeServiceIdCache() {
			serviceIdCache.add(new ServiceIdData(123456789000010L,0,101,11,1));
			serviceIdCache.add(new ServiceIdData(1111111111111111L,1111111111111999L,102,22,2));
			serviceIdCache.add(new ServiceIdData(123456789000011L,0,0,33,3));
			serviceIdCache.add(new ServiceIdData(123456789000012L,0,103,0,4));
			serviceIdCache.add(new ServiceIdData(0,0,104,0,5));
			serviceIdCache.add(new ServiceIdData(0,0,0,44,6));
	}
	
	public static int getServiceId(long gt, int ssn, int tt) {
		int serviceID = 0;

//		System.out.println("GT " + gt + " SSN " + ssn + " tt " + tt);
		
		for (ServiceIdData sd : serviceIdCache) {
//			System.out.println("========================================================");
//			System.out.println("Record - FGT " + sd.fromGT + " TGT " + sd.toGT + " SSN " + sd.ssn + " tt " + sd.tt);
			boolean f1 = false, f2=false, f3 = false;
			if ( sd.fromGT == 0 || 
				 (sd.toGT == 0 && sd.fromGT == gt) || 
				 (sd.toGT != 0 && sd.toGT >= gt && sd.fromGT <= gt)
			   ) {
				f1 = true;
//				System.out.println("F1 - FGT " + sd.fromGT + " TGT " + sd.toGT + " SSN " + sd.ssn + " tt " + sd.tt);
			}

			if (sd.ssn == 0 || sd.ssn == ssn) {
				f2=true;
//				System.out.println("F2 - FGT " + sd.fromGT + " TGT " + sd.toGT + " SSN " + sd.ssn + " tt " + sd.tt);
			}

			if (sd.tt == 0 || sd.tt == tt) {
				f3=true;
//				System.out.println("F3 - FGT " + sd.fromGT + " TGT " + sd.toGT + " SSN " + sd.ssn + " tt " + sd.tt);
			}

			if (f1 && f2 && f3)
				return sd.serviceId;
		}

		return serviceID;
	}
	

}

