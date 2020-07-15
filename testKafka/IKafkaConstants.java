/**
 * 
 */
package testKafka;

/**
 * @author Sumit.Bhatkar
 *
 */
interface IKafkaConstants {

    public static String KAFKA_BROKERS = "0.0.0.0:9092";
    public static Integer MESSAGE_COUNT=100000;
    public static String CLIENT_ID="client1";
    public static String TOPIC_NAME="TestTopic";
    public static String GROUP_ID_CONFIG="consumerGroup3";
    public static Integer MAX_NO_MESSAGE_FOUND_COUNT=10;
    public static String OFFSET_RESET_LATEST="latest";
    public static String OFFSET_RESET_EARLIER="earliest";
    public static Integer MAX_POLL_RECORDS=10;
    public static int NUMBER_OF_PARTITIONS=10;
}
