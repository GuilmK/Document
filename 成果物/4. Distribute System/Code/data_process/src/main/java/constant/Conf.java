package constant;

public interface Conf {
    // Data Source File
    String recordFilePath = "./data/record.json";

    // Kafka
    String kafkaClusterIP = "192.168.1.23:9092,192.168.1.22:9092";
    String topicName = "my-topic5";

    // Redis
    String  redisHost = "192.168.1.154";
    int  redisPort = 6379;
    String rdbKey = "rdb";//redis key
    String wrongKey = "wrong";//redis key
    String wrongChannel = "wrong_channel";
    String rightChannel = "right_channel";

    // HBase Table Name
    String recordName = "Record";
    String meetName = "MeetCount";
    String trackName = "Track";
    String invalidName = "Invalid";
}
