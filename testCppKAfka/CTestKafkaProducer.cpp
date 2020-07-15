#include <iostream>
#include <string>
#include <cstdlib>
#include <cstdio>
#include <csignal>
#include <cstring>
#include <ctime>
#include <thread>

#if _AIX
#include <unistd.h>
#endif

/*
 * Typical include path in a real application would be
 * #include <librdkafka/rdkafkacpp.h>
 */
#include "rdkafkacpp.h"

#define PRODUCE_MSG_CNT 10
#define MESSAGE_PREFIX "The message to be sent "
#define NUM_PARTITIONS 10
#define NUM_THREADS 10
#define QUE_BUFF_MAX_MSG_SIZE  "1000000"


static volatile sig_atomic_t run = 1;
std::string brokers;
std::string topic;

static void sigterm (int sig) {
  run = 0;
}

class Timer
{
public:
    Timer() { clock_gettime(CLOCK_REALTIME, &beg_); }

    double elapsed() {
        clock_gettime(CLOCK_REALTIME, &end_);
        return (end_.tv_sec - beg_.tv_sec)*1000 +
            (end_.tv_nsec - beg_.tv_nsec) / 1000000.;
    }

    void reset() { clock_gettime(CLOCK_REALTIME, &beg_); }

private:
    timespec beg_, end_;
};


class ExampleDeliveryReportCb : public RdKafka::DeliveryReportCb {
public:
  void dr_cb (RdKafka::Message &message) {
    /* If message.err() is non-zero the message delivery failed permanently
     * for the message. */
    //if (message.err())
    //  std::cerr << "% Message delivery failed: " << message.errstr() << std::endl;
    //else
    //  std::cerr << "% Message delivered to topic " << message.topic_name() <<
    //    " [" << message.partition() << "] at offset " <<
    //    message.offset() << std::endl;
	return;
  }
};

RdKafka::ErrorCode produce_msg (RdKafka::Producer *producer, std::string topic, int parition, char *line, int len)
{
	//std::cout << line << "   " << len << std::endl;
	
    /*
     * Send/Produce message.
     * This is an asynchronous call, on success it will only
     * enqueue the message on the internal producer queue.
     * The actual delivery attempts to the broker are handled
     * by background threads.
     * The previously registered delivery report callback
     * is used to signal back to the application when the message
     * has been delivered (or failed permanently after retries).
     */
    RdKafka::ErrorCode err =
      producer->produce(
                        /* Topic name */
                        topic,
                        /* Any Partition: the builtin partitioner will be
                         * used to assign the message to a topic based
                         * on the message key, or random partition if
                         * the key is not set. */
                        //RdKafka::Topic::PARTITION_UA,
						parition, 
                        /* Make a copy of the value */
                        RdKafka::Producer::RK_MSG_COPY /* Copy payload */,
                        /* Value */
                        //const_cast<char *>(line.c_str()), line.size(),
						line, len,
                        /* Key */
                        NULL, 0,
                        /* Timestamp (defaults to current time) */
                        0,
                        /* Message headers, if any */
                        NULL,
                        /* Per-message opaque value passed to
                         * delivery report */
                        NULL);

    if (err != RdKafka::ERR_NO_ERROR) 
	{
		std::cerr << "% Failed to produce to topic " << topic << ": " <<
        RdKafka::err2str(err) << std::endl;
		return err;
    } 
	//else {
      //std::cerr << "% Enqueued message (" << len << " bytes) " << "for topic " << topic << std::endl;
    //}

    /* A producer application should continually serve
     * the delivery report queue by calling poll()
     * at frequent intervals.
     * Either put the poll call in your main loop, or in a
     * dedicated thread, or call it after every produce() call.
     * Just make sure that poll() is still called
     * during periods where you are not producing any messages
     * to make sure previously produced messages have their
     * delivery report callback served (and any other callbacks
     * you register). */
    producer->poll(0);
	return RdKafka::ERR_NO_ERROR;
}

void run_producer(int thrNum)
{
	/*
	 * Create configuration object
	 */
	RdKafka::Conf *conf = RdKafka::Conf::create(RdKafka::Conf::CONF_GLOBAL);

	std::string errstr;

	/* Set bootstrap broker(s) as a comma-separated list of
	 * host or host:port (default port 9092).
	 * librdkafka will use the bootstrap brokers to acquire the full
	 * set of brokers from the cluster. */
	if (conf->set("bootstrap.servers", brokers, errstr) != RdKafka::Conf::CONF_OK) 
	{
		std::cerr << errstr << std::endl;
		exit(1);
	}
	
	std::string qsize = QUE_BUFF_MAX_MSG_SIZE;
	if (conf->set("queue.buffering.max.messages", qsize, errstr) != RdKafka::Conf::CONF_OK) 
	{
		std::cerr << errstr << std::endl;
		exit(1);
	}
	
	/* Set the delivery report callback.
	* This callback will be called once per message to inform
	* the application if delivery succeeded or failed.
	* See dr_msg_cb() above.
	* The callback is only triggered from ::poll() and ::flush().
	*
	* IMPORTANT:
	* Make sure the DeliveryReport instance outlives the Producer object,
	* either by putting it on the heap or as in this case as a stack variable
	* that will NOT go out of scope for the duration of the Producer object.
	*/
	ExampleDeliveryReportCb ex_dr_cb;

	if (conf->set("dr_cb", &ex_dr_cb, errstr) != RdKafka::Conf::CONF_OK) 
	{
		std::cerr << errstr << std::endl;
		exit(1);
	}

	/*
	* Create producer instance.
	*/
	RdKafka::Producer *producer = RdKafka::Producer::create(conf, errstr);
	if (!producer) 
	{
		std::cerr << "Failed to create producer: " << errstr << std::endl;
		exit(1);
	}

	delete conf;
  
	char line[200];
	for (int i=0; run && i<PRODUCE_MSG_CNT; i++) 
	{
		int len = sprintf (line , "%s - %d - %d",MESSAGE_PREFIX,thrNum,i);
		
		int parition = i % NUM_PARTITIONS; // there are 10 paritions
		RdKafka::ErrorCode err = produce_msg(producer, topic, parition, line, len);

		if (err == RdKafka::ERR__QUEUE_FULL) {
			/* If the internal queue is full, wait for
			* messages to be delivered and then retry.
			* The internal queue represents both
			* messages to be sent and messages that have
			* been sent or failed, awaiting their
			* delivery report callback to be called.
			*
			* The internal queue is limited by the
			* configuration property
			* queue.buffering.max.messages */
			producer->poll(1000/*block for max 1000ms*/);
			produce_msg(producer, topic, parition, line, len);  // retry
		}
	}
	
	/* Wait for final messages to be delivered or fail.
	* flush() is an abstraction over poll() which
	* waits for all messages to be delivered. */
	std::cerr << "% Flushing final messages..." << std::endl;
	producer->flush(10*1000 /* wait for max 10 seconds */);

	if (producer->outq_len() > 0)
	{
		std::cerr << "% " << producer->outq_len() << "message(s) were not delivered" << std::endl;
	}

	delete producer;
	return;
}

int main (int argc, char **argv) {

	if (argc != 3) 
	{
		std::cerr << "Usage: " << argv[0] << " <brokers> <topic>\n";
		exit(1);
	}

	brokers = argv[1];
	topic = argv[2];

	signal(SIGINT, sigterm);
	signal(SIGTERM, sigterm);

	std::thread *threadsArr[NUM_THREADS]; 

	Timer tmr;
	for (int i=0; i < NUM_THREADS; i++)
	{
		threadsArr[i] = new std::thread(run_producer,i);
	}
	
	for (int i=0; i < NUM_THREADS; i++)
	{
		threadsArr[i]->join();
	}
	
	//run_producer();

	double t = tmr.elapsed();
	std::cout << "10M records : " << NUM_THREADS << " threads prod / 10 partition :: " << t << " msec"<< std::endl;

	return 0;
}