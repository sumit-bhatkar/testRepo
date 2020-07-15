package javatest.testDateFormat;

import java.sql.Timestamp;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;

public class TestDateFormat {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		System.out.println("//////////////////////////////////////////////////////////");
		String date = new java.text.SimpleDateFormat("dd-MM-yyyy HH").format(new java.util.Date (1526580425000L));
		System.out.println("DATE IS " + date);
		//		Calendar cal=Calendar.getInstance();
		Calendar cal=new GregorianCalendar() ;

		System.out.println("HOUR IS -  " + cal.get(Calendar.HOUR_OF_DAY));
		System.out.println("//////////////////////////////////////////////////////////");

		DateFormat 	formatter 	= null ;
		Date		date1 		= null ;
		Long 		timeInLong  = 0l ;
		try {
			formatter 	= new SimpleDateFormat("yyyyMMddHHmmss") ;
			date1		= formatter.parse("20180517233705") ;
			timeInLong	= date1.getTime() ;
			System.out.println("DATE IS " + timeInLong);
			try
			{
				System.out.println(new SimpleDateFormat("dd-MMM-yy HH.mm.ss.000000 aa").
						format(new java.util.Date(Long.parseLong(""+timeInLong)))) ;
			}
			catch (Exception e)
			{
				e.printStackTrace();
			}
		} catch (ParseException e) 
		{
			e.printStackTrace();
		}
		System.out.println("//////////////////////////////////////////////////////////");
		try {
			SimpleDateFormat dateFormat = new SimpleDateFormat("dd-MM-yyyy HH");
			Date parsedDate = dateFormat.parse(date);
			Timestamp timestamp = new java.sql.Timestamp(parsedDate.getTime());
			long dateLong = timestamp.getTime();
			System.out.println("Timestamp converted back " + dateLong);
			
		} catch(Exception e) { 
			//this generic but you can control another types of exception
			// look the origin of excption 
			System.out.println("Exception IS " + e.toString());
		}
				

	}

}
