package main;

import constant.Conf;
import kafka.Consumer;
import kafka.MyProducer;
import redis.MySubThread;
import redis.Subscriber;
import redis.clients.jedis.Jedis;

public class NewMain {
    public static void main(String[] args) {
        new Thread(new MyProducer()).start();
        new Thread(new Consumer()).start();
        new Thread(new MySubThread(
                new Jedis(Conf.redisHost, Conf.redisPort),
                Conf.rightChannel, new Subscriber(Conf.recordName))).start();
        new Thread(new MySubThread(
                new Jedis(Conf.redisHost, Conf.redisPort),
                Conf.wrongChannel, new Subscriber(Conf.invalidName))).start();
    }
}
