package main;

import com.google.gson.Gson;
import data.Record;
import hbase.HBaseCreateOP;
import hbase.HBaseInsert;
import kafka.ConsumerThread;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.consumer.OffsetAndMetadata;
import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.TopicPartition;
import redis.MyPubThread;
import redis.MySubThread;
import redis.Subscriber;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.Pipeline;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

public class Main {


	private static String rdbKey = "rdb";//redis key
	private static String wrongKey = "wrong";//redis key
	private static String  redisHost = "192.168.1.154";
	private static int  redisPort = 6379;
	private static String topicName = "my-topic1";
	private static String topicName2 = "wrong-topic1";
	private static String kafkaClusterIP = "192.168.1.23:9092,192.168.1.22:9092";
	private static String recordFilePath = "./data/record.json";

	private static Jedis jedis = new Jedis(redisHost,redisPort);
	private static HBaseInsert in = new HBaseInsert();


	static void jsonToKafka() throws IOException {
		Properties props = new Properties();
		props.put("bootstrap.servers", kafkaClusterIP);//kafka clusterIP
		props.put("acks", "1");
		props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
		props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
		Producer<String, String> producer = new KafkaProducer<>(props);
		BufferedReader br =  new BufferedReader(new FileReader(recordFilePath));
		int i = 0;//record key
		String record;
		//send record to kafka
//		int cnt = 0;
		String[] tmp;int leng;double longi,lati;
		//send record to kafka
		while((record = br.readLine())!=null) {
			tmp = record.split(",");
			leng = tmp[tmp.length-2].substring(12).length();
			longi = Double.parseDouble(tmp[tmp.length-2].substring(12).substring(0,leng - 2));
			leng = tmp[tmp.length-1].substring(11).length();
			lati = Double.parseDouble(tmp[tmp.length-1].substring(11).substring(0,leng - 2));
			if((longi < 130 && lati < 40))
			{
				producer.send(new ProducerRecord<String, String>(topicName, Integer.toString(i), record), new Callback()
				{
					public void onCompletion(RecordMetadata metadata, Exception e)
					{
						if (e != null)
							e.printStackTrace();
						//System.out.println("The offset of the record we just sent is: " + metadata.offset());
					}
				});
				i++;
			}
			else
			{
				producer.send(new ProducerRecord<String, String>(topicName2, Integer.toString(i), record), new Callback()
				{
					public void onCompletion(RecordMetadata metadata, Exception e)
					{
						if (e != null)
							e.printStackTrace();
						//System.out.println("The offset of the record we just sent is: " + metadata.offset());
					}
				});
			}

		}
		br.close();
		producer.close();
	}

	static void kafkaToRedis(){
		new ConsumerThread();
	}

//	static void kafkaToRedis(){
//		Properties props = new Properties();
//		Pipeline pipelineq = jedis.pipelined();
//		props.put("bootstrap.servers", kafkaClusterIP);//kafka clusterIP
//		props.put("group.id", "test");
//		props.put("enable.auto.commit", "true");
//		props.put("auto.offset.reset", "earliest");
//		props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
//		props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
//		KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
//		consumer.subscribe(Arrays.asList(topicName));
//
//		int cnt = 0;
//		while (true) {
//			System.out.println("True ~~~");
//			cnt++;
//			if (cnt == 100) break;
//			ConsumerRecords<String, String> records = consumer.poll(100);
//			for (ConsumerRecord<String, String> record : records){
//				System.out.printf("offset = %d, key = %s, value = %s%n", record.offset(), record.key(), record.value());
//				pipelineq.sadd(key,record.value());//record to redis
//			}
//		}
//		try {
//			pipelineq.close();
//		} catch (IOException e) {
//			e.printStackTrace();
//		}
//	}


	static void redisToHbase() throws IOException {
//		jedis.close();
		List<Record> wrongList = new ArrayList<>();
		List<Record> rdbList = new ArrayList<>();
		Record record;
		Gson gson = new Gson();
		for(String jsonString : jedis.smembers(rdbKey)){
			System.out.println(jsonString);
			record = gson.fromJson(jsonString,Record.class);
			rdbList.add(record);
		}
		for(String jsonString : jedis.smembers(wrongKey)){
			System.out.println(jsonString);
			record = gson.fromJson(jsonString,Record.class);
			wrongList.add(record);
		}

		in.insertRecordsToHBase("Record", rdbList);
		in.insertRecordsToHBase("Invalid", wrongList);
	}

	public static void main(String[] args) throws IOException {


		/*
		1.发送record至kafka
		 */
		jsonToKafka();
		System.out.println("Json TO Kafka finish");

		/*
		2.将kafka中的信息写入redis
		 */
		kafkaToRedis();
		System.out.println("Kafka to Redis finish");

		/*
		3.在HBase中创建数据库(创建一次)
		 */
//		 HBaseCreateOP.main(args);

		/*
		4.将redis中的数据发送至HBase
		 */
//		redisToHbase();
//		System.out.println("Redis to HBase finish");

	}
}
