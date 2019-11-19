package redis;

import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPubSub;

public class MySubThread extends Thread {
	private Jedis myJedis=null;
	private String myChannel="";
	private JedisPubSub myJedisPubSub=null;
	   
	public MySubThread(Jedis jedis, String channel, JedisPubSub jedispubsub) {
		myJedis=jedis;
		myChannel=channel;
		myJedisPubSub=jedispubsub;
	}

	@Override
	public void run() {
		myJedis.subscribe(myJedisPubSub, myChannel);
	}

}
