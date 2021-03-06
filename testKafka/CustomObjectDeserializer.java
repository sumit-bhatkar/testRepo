package testKafka;

import java.util.Map;
import org.apache.kafka.common.serialization.Deserializer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.fasterxml.jackson.databind.ObjectMapper;
//import com.gaurav.kafka.pojo.CustomObject;

public class CustomObjectDeserializer implements Deserializer<String> {
	
	public void configure(Map<String, ?> configs, boolean isKey) {
	}
	
	public String deserialize(String topic, byte[] data) {
		ObjectMapper mapper = new ObjectMapper();
		String object = null;
		try {
			object = mapper.readValue(data, String.class);
		} catch (Exception exception) {
			System.out.println("Error in deserializing bytes "+ exception);
		}
		return object;
	}
	@Override
	public void close() {
	}
}
