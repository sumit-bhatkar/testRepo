/**
 * 
 */
package testKafka;

import java.util.Map;

import org.apache.kafka.clients.producer.Partitioner;
import org.apache.kafka.common.Cluster;

/**
 * @author Sumit.Bhatkar
 *
 */
class CustomSerializer {


	  private static final int PARTITION_COUNT=50;
	  
	  public void configure(Map<String, ?> configs) {
	  }
	  
	  public int partition (String topic, Object key, byte[] keyBytes, Object value, byte[] valueBytes, Cluster cluster) {
	    Integer keyInt=Integer.parseInt(key.toString());
	    return keyInt % PARTITION_COUNT;
	  }
	  
	  public void close() {
	  }
}
