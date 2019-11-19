package kafka;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Properties;

import constant.Conf;
import org.apache.kafka.clients.producer.*;

public class MyProducer implements Conf,Runnable
{
    private String topicName = Conf.topicName;

    public void sendRecords() throws IOException, InterruptedException {

    }

    @Override
    public void run(){
        Properties props = new Properties();
        props.put("bootstrap.servers", "192.168.1.22:9092,192.168.1.23:9092");//kafka clusterIP
        props.put("acks", "1");
        props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        try {
            BufferedReader br =  new BufferedReader(new FileReader("./data/record.json"));//record file path
            Producer<String, String> producer = new KafkaProducer<>(props);
            int i = 0;//message key
            String record;
            //send record to kafka
            while((record = br.readLine())!=null) {
                producer.send(new ProducerRecord<String, String>(topicName, Integer.toString(i), record), new Callback() {
                    public void onCompletion(RecordMetadata metadata, Exception e) {
                        if (e != null)
                            e.printStackTrace();
//                        System.out.println("The offset of the record we just sent is: " + metadata.offset());
                    }
                });
                i++;

                if (i%500 == 0) {
                    System.out.println("Producer" + i);
                    Thread.sleep(1000);
                }
            }
            br.close();
            producer.close();
        }catch(Exception e)
        {
            System.out.println("something wrong");
        }
    }

}