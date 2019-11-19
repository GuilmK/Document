package kafka;

import java.util.Arrays;
import java.util.Properties;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;

import constant.Conf;
import redis.MyPubThread;
import redis.MySubThread;
import redis.Subscriber;
import redis.clients.jedis.Jedis;
public class Consumer implements Runnable{

    int leng;
    String[] tmp;
    double longi,lati;

    @Override
    public void run() {
        Properties props = new Properties();
        props.put("bootstrap.servers", Conf.kafkaClusterIP);//kafka clusterIP
        props.put("group.id", "test");
        props.put("enable.auto.commit", "true");
        props.put("auto.offset.reset", "earliest");
        props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");

        KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
        consumer.subscribe(Arrays.asList(Conf.topicName));

        Jedis jedis = new Jedis(Conf.redisHost, Conf.redisPort);

        while (true)
        {
            ConsumerRecords<String, String> records = consumer.poll(100);
            for (ConsumerRecord<String, String> record : records)
            {
//                System.out.printf("offset = %d, key = %s, value = %s%n", record.offset(), record.key(), record.value());

                tmp = record.value().split(",");
                leng = tmp[tmp.length-2].substring(12).length();
                longi = Double.parseDouble(tmp[tmp.length-2].substring(12).substring(0,leng - 2));
                leng = tmp[tmp.length-1].substring(11).length();
                lati = Double.parseDouble(tmp[tmp.length-1].substring(11).substring(0,leng - 2));

                if((longi < 130 && lati < 40))
                {
                    jedis.publish(Conf.rightChannel, record.value());
                }
                else {
                    jedis.publish(Conf.wrongChannel, record.value());
                }

            }
        }
    }

}