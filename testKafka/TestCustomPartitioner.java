package testKafka;

import java.util.Map;

import org.apache.kafka.clients.producer.Partitioner;
import org.apache.kafka.common.Cluster;

public class TestCustomPartitioner implements Partitioner{

	public TestCustomPartitioner() {
	}

	public int partition(String topic, Object key, byte[] keyBytes, Object value, byte[] valueBytes, 
			Cluster cluster) {

		return (int)((Long) key % IKafkaConstants.NUMBER_OF_PARTITIONS);
	}

	public void close() {

	}

	public void configure(Map<String, ?> arg0) {
		// TODO Auto-generated method stub

	}
}
