package javatest.testStringSplit;

public class TestStringSplit {

	public static void main(String[] args) {
		System.out.println("//////////////////////////////////////////////////////////");
			
		String formatedCos0 = getFormattedCosId(0);
		String formatedCos1 = getFormattedCosId(1);
		System.out.println("Get formated cosid [" + formatedCos0 + "]");
		System.out.println("Get formated cosid [" + formatedCos1 + "]");
		
		System.out.println("//////////////////////////////////////////////////////////");
		
		int cos0 = getFormattedCosId(formatedCos0);
		System.out.println("Get cosid [" + cos0 + "]");
		int cos1 = getFormattedCosId(formatedCos1);
		System.out.println("Get cosid [" + cos1 + "]");
		
		System.out.println("//////////////////////////////////////////////////////////");
	}
	
	
	public static int getFormattedCosId(String cosIdString)
	{
		String[] fields = split(cosIdString, '#');

		if (fields == null ) {
			return 0;
		}
		
		if (fields.length >= 3) {
			System.out.println("Split is [" + fields[2] + "]" + fields.length);
			return Integer.parseInt(fields[2]);
		}
		else
		{
			System.out.println("length is [" + fields.length + "]");
		}
		return 0;
	}
	
	public static String getFormattedCosId(int cosId)
	{
		StringBuffer sb = new StringBuffer();
		if(cosId == 0)
		{
			sb.append("#").append(0).append("#");
		}
		else
		{
			sb.append("#").append(0).append("#").append(cosId).append("#");
		}
		return sb.toString();
	}
	
//////////////////////////////////////////////////////////////////////////////////////////////////
//	From Imas String splitter
//////////////////////////////////////////////////////////////////////////////////////////////////	
		public static final int            MAX_TOKENS = 1024 ;

		/**
		 * Splits a string into tokens based on a delimiter.
		 * The tokens are set into the output list
		 * 
		 * @param s String to split
		 * @param delim Delimiter
		 * @param output String list in which to set the tokens
		 * @param maxTokens Maximum amount of tokens to extract from the String
		 *  
		 * @return Number of tokens extracted from the String
		 */
		public static int split(String s, char delim, String[] output, int maxTokens)
		{
			char[]          chrArray = s.toCharArray() ;
			int             offset = 0 ;
			int             length = 0 ;
			int             start = 0 ;
			int             len = 0 ;

			while (offset < chrArray.length && length < maxTokens)
			{
				start = offset ;
				len = 0 ;
				while (offset < chrArray.length && chrArray[offset] != delim)
				{
					offset++ ;
					len++ ;
				}

				offset++ ;
				output[length++] = new String(chrArray, start, len) ;
			}

			return length ;
		}

		/**
		 * Splits a string into tokens based on a delimiter.
		 * The tokens are set into the output list. The maximum
		 * tokens extracted are limited to the length of output list
		 * 
		 * @param s String to split
		 * @param delim Delimiter
		 * @param output String list in which to set the tokens
		 * 
		 * @return  Number of tokens extracted from the String
		 */
		public static int split(String s, char delim, String[] output)
		{
			return split(s, delim, output, output.length) ;
		}

		/**
		 * Returns a list of tokens split based on a delimiter.
		 * The maximum number of tokens returned is restricted by the
		 * value of StringSplitter.MAX_TOKENS
		 * 
		 * @param s String to split
		 * @param delim Delimiter
		 * 
		 * @return Token list
		 */
		public static String[] split(String s, char delim)
		{
			String[]    output = new String[MAX_TOKENS] ;
			int         len = split(s, delim, output, MAX_TOKENS) ;

			String[]    ret = new String[len] ;
			System.arraycopy(output, 0, ret, 0, len) ;
			return ret ;
		}

		/**
		 * The main difference of this function and split() is in the number of tokens returned.
		 * <p>Consider an input string &quot;A,B,C,D&quot; and &quot;A,B,C,D,&quot; - considering
		 * ',' as the delimiter, the split() function would return 4 tokens for both of
		 * these two strings. And that is because if there is no data after the last delimiter in a
		 * string, split() does not acknowledge the presence of an empty token.</p>
		 * <p>This function, split2(), will return 4 and 5 for the two example strings respectively.
		 * This makes token counting predictable.</p>
		 */
		public static String[] split2(String s, char delim)
		{
			if (s == null)
				return new String[0] ;

			final int   LEN = s.length() ;
			int         count = 1 ;

			for (int i = 0 ; i < LEN ; i++)
			{
				if (s.charAt(i) == delim)
					count++ ;
			}

			String[]    output = new String[count] ;
			int         startAt = 0, j = 0 ;

			for (int i = 0 ; i < LEN ; i++)
			{
				if (s.charAt(i) == delim)
				{
					output[j++] = s.substring(startAt, i) ;
					startAt = i+1 ;
				}
			}
			output[j] = s.substring(startAt) ;
			return output ;
		}

}
