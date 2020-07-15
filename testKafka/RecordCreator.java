package testKafka;

import java.util.concurrent.ExecutionException;

import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;

public class RecordCreator extends Thread{
	int id;

	public RecordCreator (int i){
		id = i;
	}

	public RecordCreator (){
		id = 1000;
	}

	public void run(){
		v2();
	}
	
	public void v2 () {
		Producer<Long, String> producer = ProducerCreator.createProducer();
		Integer messageCount=2000;
		for (int index = 0; index < messageCount; index++) {
			producer.send(new ProducerRecord<Long, String>(IKafkaConstants.TOPIC_NAME, 
					new Long( index),
					"This is record "+ id + "___" + index));
		}
	}
	
//	public void v1 () { 
//		//		System.out.println("Producer" + id + " running");
//		Producer<Long, String> producer = ProducerCreator.createProducer();
//		//		long start = System.nanoTime();
//		Integer messageCount=2000;
//		for (int index = 0; index < messageCount; index++) {
//			ProducerRecord<Long, String> record = new ProducerRecord<Long, String>(IKafkaConstants.TOPIC_NAME,
//					"This is record "+ id + "___" + index);
//			try {
//				RecordMetadata metadata = producer.send(record).get();
//				//				System.out.println("Record sent with key " + index + " to partition " + metadata.partition()
//				//				+ " with offset " + metadata.offset());
//			} 
//			catch (ExecutionException e) {
//				System.out.println("Error in sending record");
//				System.out.println(e);
//			} 
//			catch (InterruptedException e) {
//				System.out.println("Error in sending record");
//				System.out.println(e);
//			}
//		}
//	}
}
