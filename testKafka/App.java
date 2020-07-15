package testKafka;

import java.time.Duration;
import java.util.concurrent.ExecutionException;
import org.apache.kafka.clients.consumer.Consumer;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;


//import testKafka.ConsumerCreator;
//import testKafka.IKafkaConstants;
//import testKafka.ProducerCreator;
//import testKafka.RecordCreator;



public class App {
	public static int THREAD_COUNT = 50;
	
	public static void main(String[] args) {
		System.out.println("Started Loop ###########################");
		Thread [] threads = new Thread [THREAD_COUNT];
		
		long start = System.nanoTime();
		
	    for (int i = 0; i < THREAD_COUNT; i++){
	        threads[i] = new Thread(new RecordCreator(i));
	        threads[i].start();
	    }
	    for (int i = 0; i < THREAD_COUNT; i++) {
	    	try {
				threads[i].join();
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
	    }
	
		long end = System.nanoTime();
		long timeElapsed = end - start;
		System.out.println("Elapsed time : [" + timeElapsed/1000/1000 + "]" );
		System.out.println("Done Loop ###########################");
		//runProducer();
		//runConsumer();
	}

	static void runConsumer() {
		Consumer<Long, String> consumer = ConsumerCreator.createConsumer();
		int noMessageFound = 0;
		long start = System.nanoTime();
		while (true) {
			ConsumerRecords<Long, String> consumerRecords = consumer.poll(Duration.ofMillis(10));
			// 10 is the time in milliseconds consumer will wait if no record is found at broker.
//			System.out.println("Entered Loop ###########################");
			if (consumerRecords.count() == 0) {
				noMessageFound++;
				if (noMessageFound > IKafkaConstants.MAX_NO_MESSAGE_FOUND_COUNT)
					// If no message found count is reached to threshold exit loop.  
					break;
				else
					continue;
			}
			//print each record. 
			consumerRecords.forEach(record -> {
				System.out.println("Record Key " + record.key());
				System.out.println("Record value " + record.value());
				System.out.println("Record partition " + record.partition());
				System.out.println("Record offset " + record.offset());
			});
			// commits the offset of record to broker. 
			consumer.commitAsync();
		}
		consumer.close();
		long end = System.nanoTime();
		long timeElapsed = end - start;
//		System.out.println("Elapsed time : [" + timeElapsed/1000/1000 + "]" );

	}

	static void runProducer() {
		
		Producer<Long, String> producer = ProducerCreator.createProducer();
//		long start = System.nanoTime();
		Integer messageCount=1000;
		for (int index = 0; index < messageCount; index++) {
			ProducerRecord<Long, String> record = new ProducerRecord<Long, String>(IKafkaConstants.TOPIC_NAME,
					"This is record " + index);
			try {
				RecordMetadata metadata = producer.send(record).get();
//				System.out.println("Record sent with key " + index + " to partition " + metadata.partition()
//				+ " with offset " + metadata.offset());
			} 
			catch (ExecutionException e) {
				System.out.println("Error in sending record");
				System.out.println(e);
			} 
			catch (InterruptedException e) {
				System.out.println("Error in sending record");
				System.out.println(e);
			}
		}
//		long end = System.nanoTime();
//		long timeElapsed = end - start;
//		System.out.println("Elapsed time : [" + timeElapsed/1000/1000 + "]" );
	}
}