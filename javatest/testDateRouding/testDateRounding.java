package javatest.testDateRouding;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;

public class testDateRounding {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
//		long tm = System.currentTimeMillis();
		String givenDateString = "Tue Apr 30 13:36:19 GMT+05:30 2013";
		long tm = convertToEpoc(givenDateString);
		System.out.println("time  = [" + tm + "]");
		System.out.println("//////////////////////////////////////////////////////////");
		System.out.println("CHECK actual" +  new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new java.util.Date(tm)) );
		
		System.out.println("CHECK hrly" +  new SimpleDateFormat("yyyy-MM-dd HH:00:00").format(new java.util.Date(tm)) );
		
//		int res = getNear15Minute(0);
//		System.out.println("Min = [" + res + "]");
		long res1 = roundUp15MinuteEPOC(tm);
		System.out.println("CHECK Min" +  new SimpleDateFormat("yyyy-MM-dd HH:mm:00").format(new java.util.Date(res1)) );
		System.out.println("//////////////////////////////////////////////////////////");
		int min = getMinOfDayFromEpochTime(res1);
		int hr = getHourOfDayFromEpochTime(res1);
		
		System.out.println("For " +  givenDateString + "  >>> Hr = " + hr + " and Min  = " +min );
		System.out.println(new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new java.util.Date(res1)));
		System.out.println("Hash Key = " + getKeyEpochTime(res1) );
		
		

	}
	
	public static long roundUp15MinuteEPOC(long time){
		time  += (15*60*1000) - (time % (15*60*1000));
		return (time );
    }
	
	public static int getNear15Minute(int minutes){
        int mod = minutes%15; 
        System.out.println("MOD = [" + mod + "]");
        int res = 0 ;
//        if((mod) >=8){
//            res = minutes+(15 - mod);
//        }else{
//            res = minutes-mod;
//        }
        if (mod >0)
        	res = minutes+(15 - mod);
        else
        	res = minutes;
        return (res%60);
    }
	
	public static int getMinOfDayFromEpochTime(long startTime) {
		Calendar cal = Calendar.getInstance(); 
		cal.setTime(new Date(startTime));
		return (cal.get(Calendar.MINUTE));
	}
	
	public static int getHourOfDayFromEpochTime(long startTime) {
		Calendar cal = Calendar.getInstance(); 
		cal.setTime(new Date(startTime));
		return (cal.get(Calendar.HOUR_OF_DAY));
	}
	
	public static long convertToEpoc(String time)
	{
//		String givenDateString = "Tue Apr 23 16:08:28 GMT+05:30 2013"; 
		long timeInMilliseconds = 0;
		SimpleDateFormat sdf = new SimpleDateFormat("EEE MMM dd HH:mm:ss z yyyy");
		try {
			Date mDate = sdf.parse(time);
			timeInMilliseconds = mDate.getTime();
			System.out.println("Date in milli :: " + timeInMilliseconds);
		} catch (ParseException e) {
			e.printStackTrace();
		}
		return timeInMilliseconds;
	}
	
	public static int getKeyEpochTime(long startTime) {
//		Calendar cal = Calendar.getInstance(); 
//		cal.setTime(new Date(startTime));
//		int yr = cal.get(Calendar.YEAR);
//		int mon = cal.get(Calendar.MONTH);
//		int day = cal.get(Calendar.DAY_OF_MONTH);
//		int hr = cal.get(Calendar.HOUR_OF_DAY);
//		int min = cal.get(Calendar.MINUTE);
//		int i = min + hr *100 + day * 10000 + mon * 1000000;
		
		System.out.println("ASD " + new SimpleDateFormat("ddHHmm").format(startTime));
		return Integer.valueOf(new SimpleDateFormat("ddHHmm").format(startTime));
	}


}
