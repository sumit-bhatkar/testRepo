package javatest.testThreadTimer;

import java.util.Calendar;
import java.util.GregorianCalendar;
import java.util.Random;



public class TestTimer {
	static {
		RegisExpiryChecker regisExpiryChecker = new RegisExpiryChecker();
		Thread t = new Thread(regisExpiryChecker, "RegisExpiryChecker");
		t.start();
		RegisExpiryChecker.lastExpIndex = RegisExpiryChecker.getExpIndex();
		Calendar cal = Calendar.getInstance();
		System.out.println("Start expiryMin " + RegisExpiryChecker.lastExpIndex + "  Start sec " + cal.get(Calendar.SECOND));
		System.out.println("=================================================");
	}

	public static void main(String[] args) 
	{
//		print();
	}

	public static int getMinuteOfDay() 
	{
		Calendar cal = Calendar.getInstance();
		int min = cal.get(Calendar.HOUR_OF_DAY) * 60 + cal.get(Calendar.MINUTE);
		return min;
	}

	public static void print() {
		System.out.println("=================================================");
		Calendar calendar = Calendar.getInstance(); 
		System.out.println("getTimeInMillis " + calendar.getTimeInMillis());
		System.out.println("System.currentTimeMillis() " + System.currentTimeMillis());
		System.out.println("getMinuteOfDay " + getMinuteOfDay()); 
		System.out.println("sec " + calendar.get(Calendar.SECOND));
		System.out.println("=================================================");
	}

	static class RegisExpiryChecker implements Runnable 
	{
		static int lastExpIndex = 0;
		static int worktime = 15;
		@Override
		public void run() 
		{
			while (true)
			{
				int reg_expiry_interval = 1;
				try 
				{
					int sleepSec = getSleepSeconds();
					System.out.println("Sleeping for " + sleepSec);
					 Thread.sleep(reg_expiry_interval*sleepSec*1000);
    				 runRegisExpiryLogic();
    				 System.out.println("=================================================");
				} catch (Exception e) {
					System.out.println("Error while executing RegisExpiryChecker");
				}
			}
		}

		private void runRegisExpiryLogic() 
		{
			int expiryIndex = getExpIndex();
			Boolean flag = false;
			Calendar cal = Calendar.getInstance();
			
			if (expiryIndex != lastExpIndex+1)
			{
				System.out.println("########### Mar Gaye #### exp" + expiryIndex + "last " + lastExpIndex);
				expiryIndex = lastExpIndex + 1;
				flag = true;
			}
			
			System.out.println("expiryMin " + expiryIndex + " sec " + cal.get(Calendar.SECOND) +
					" Working for " + worktime);
			lastExpIndex=expiryIndex;
			
			long startTime = System.currentTimeMillis();
			try 
			{
				 Thread.sleep(worktime*1000);
				 worktime+=30;
				 if (worktime > 130) worktime=15;
				 
			} catch (Exception e) {
				System.out.println("Error while executing RegisExpiryChecker");
			}
			long endTime = System.currentTimeMillis();
			if ((endTime - startTime) > 60*1000)
			{
				//TODO : Since it took long to expire last batch, one expiry slot will be skipped
				// logic to be fixed to expire the skipped slot before sleeping
				System.out.println("RegLog: Expiration took more than min - Possible Memory leak");
			
			}
			
			if (flag)
			{
				System.out.println("Looping exp logic");
				runRegisExpiryLogic();
				
			}
			
		}
		
		public static int getExpIndex() 
		{
			int minuteOfDay = getMinuteOfDay();
			int expiryIndex = 0;
			if(minuteOfDay == 0)
			    expiryIndex = 1439;
			else
				expiryIndex = minuteOfDay - 1;
	

			return expiryIndex;
		}
		
		public static int getSleepSeconds() 
		{
//			int minuteOfDay = getMinuteOfDay();
//			int expiryIndex = 0;
//			if(minuteOfDay == 0)
//			    expiryIndex = 1439;
//			else
//				expiryIndex = minuteOfDay - 1;
//	
			Calendar cal = Calendar.getInstance();
			return 60 - cal.get(Calendar.SECOND);
		}
	}
	
	   

}
