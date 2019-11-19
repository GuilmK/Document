package redis;

import java.util.ArrayList;
import java.util.List;

import com.google.gson.Gson;
import data.Record;
import hbase.HBaseInsert;
import hbase.HBaseInsertUtil;
import hbase.RecordMap;
import redis.clients.jedis.JedisPubSub;

public class Subscriber extends JedisPubSub {
	private String get_message="";
	public  String toString() {
		return get_message;
	}
	private String tablename;

    public Subscriber(String tablename) {
        this.tablename = tablename;
    }

    public void onMessage(String channel, String message) {
        HBaseInsertUtil.insert(tablename, new Gson().fromJson(message, Record.class));
    }
    
    public void onSubscribe(String channel, int subscribedChannels) {
        System.out.println(String.format("@@@@ %s, subscribedChannels %d",
                channel, subscribedChannels));
    }
    
    public void onUnsubscribe(String channel, int subscribedChannels) {
        System.out.println(String.format("unsubscribe redis channel, channel %s, subscribedChannels %d", 
                channel, subscribedChannels));
    }
}
