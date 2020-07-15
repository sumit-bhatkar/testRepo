package javatest.test2;


public class TestGGSNUsage {

	public static void main(String[] args) {
		System.out.println("========== START ==============");  
		
	   	String subrecordStr = "11;1514454004000;1514454106000;102;0008000040;;1514454107000;142;80;;334|20|402|18945$8;1514453942000;1514453947000;5;0008000040;;1514454107000;80;111;;334|20|402|18945" ;
		String[] subRecord = subrecordStr.split("\\$") ;
			
 		if(subRecord == null || subRecord.length == 0)
		{
 			System.out.println("Unreachable");  
		}
		else
		{
			long totalUsage=0;
			for(String record : subRecord)
			{
//				System.out.println("Rec = [" + record + "]");
				totalUsage = totalUsage + getUsage(record);
			}
			System.out.println("Total Usage = [" + totalUsage + "]"); 
		}
		
 		
		
		System.out.println("==========  END  ==============");   

	}
	
	private static long getUsage (String record) 
	{
		long uplink = 0;
		long downlink = 0;
		long total = 0;
		String[] spliteRecord = null ;
		try
    	{
    		if(record != null && record.trim().length() != 0)
        	{
        		spliteRecord = record.split(";",11)  ;
//        		System.out.println("Rec = [" + record + "]");
        	}
			
			if(spliteRecord != null && spliteRecord.length != 0)
			{
			    
				if(spliteRecord[7] != null && spliteRecord[7].trim().length() != 0)
				{
					System.out.println("Rec 7 = [" + spliteRecord[7] + "]");
					String up = spliteRecord[7];
					uplink = Long.parseLong("80");
					System.out.println("uplink = [" + uplink + "]" );
				}
				
				if(spliteRecord[8] != null && spliteRecord[8].trim().length() != 0)
				{
					System.out.println("Rec 8 = [" + spliteRecord[8] + "]");
					downlink = Long.parseLong(spliteRecord[8]);
				}
				System.out.println("total = [" + uplink + "]" + downlink);
				total = uplink + downlink;
			}
		}  
//		catch(ExecException ex)
//		{
//			logger.error("Execption while processing preprocessor: " + ex.getLocalizedMessage()) ;	
//			return 0;
//		}
		catch(Exception ex)
		{
			System.out.println("Execption while processing preprocessor: " + ex.getMessage()) ;
			return 0;
		}
		return total;
	}

}
