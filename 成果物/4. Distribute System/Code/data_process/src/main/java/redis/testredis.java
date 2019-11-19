package redis;

import redis.clients.jedis.Jedis;

public class testredis {
	public static void main(String[] args) {
		String redisIp="192.168.56.101";
		int redisPort=6379;
		String channel="redischat";
		String message="Hello world!";
//		testRedisClient.getMessage(channel,new Subscriber());		
//		MySubThread testSubTread=new MySubThread(new Jedis(redisIp,redisPort),channel,new Subscriber());
//		testSubTread.start();
		for(int i=0;i<50;i++) {
			MyPubThread testPubThread=new MyPubThread(new Jedis(redisIp,redisPort),channel,message+i);
			testPubThread.start();
		}
	}
}
