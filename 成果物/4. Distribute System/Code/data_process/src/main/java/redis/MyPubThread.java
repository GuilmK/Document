package redis;

import redis.clients.jedis.Jedis;

public class MyPubThread extends Thread{
	private Thread t;
	private Jedis myJedis=null;
	private String myChannel="";
	private String message="";
	
	public MyPubThread(Jedis jedis,String channel,String s) {
		myJedis=jedis;
		myChannel=channel;
		message=s;
	}
	
	public void run() {
		myJedis.publish(myChannel, message);
		System.out.println(":"+message);
	}
	
	public void start () {
		if (t == null) {
			t = new Thread (this);
			t.start ();
		}
	}
}
