package hbase;

import data.Record;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class HBaseInsertUtil {
    private static final String FAMILY_NAME = "info";  //给出的用例中只有一个Record表，表中只有一个info列族

    public static boolean insert(String tableName, Record record) {
        //1.确定行键 （placeID##time##eid）
        String rowKey = record.getPlaceId() + "##" + record.getTime() + "##" + record.getEid();

        Put put = new Put(Bytes.toBytes(rowKey));
        //2.添加列
        put.addColumn(Bytes.toBytes(FAMILY_NAME) , Bytes.toBytes("placeId") , Bytes.toBytes(record.getPlaceId()+""));
        put.addColumn(Bytes.toBytes(FAMILY_NAME) , Bytes.toBytes("time") , Bytes.toBytes(record.getTime()+""));
        put.addColumn(Bytes.toBytes(FAMILY_NAME) , Bytes.toBytes("address") , Bytes.toBytes(record.getAddress()));
        put.addColumn(Bytes.toBytes(FAMILY_NAME) , Bytes.toBytes("longitude") , Bytes.toBytes(record.getLongitude()+""));
        put.addColumn(Bytes.toBytes(FAMILY_NAME) , Bytes.toBytes("latitude") , Bytes.toBytes(record.getLatitude()+""));

        //3.执行数据库插入操作
        Table table = HBaseConf.getTableByName(tableName);
        try {
            table.put(put);
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        }
        return true;
    }

    public static boolean insertAll(String tableName, List<Record> records) {
        List<Put> allPuts = new ArrayList<>();
        for(Record record : records) {
            //1.确定行键 （placeID##time##eid）
            String rowKey = record.getPlaceId() + "##" + record.getTime() + "##" + record.getEid();
//            String rowKey = record.getEid();
            Put put = new Put(Bytes.toBytes(rowKey));
            //2.添加列
            put.addColumn(Bytes.toBytes(FAMILY_NAME) , Bytes.toBytes("placeId") , Bytes.toBytes(record.getPlaceId()+""));
            put.addColumn(Bytes.toBytes(FAMILY_NAME) , Bytes.toBytes("time") , Bytes.toBytes(record.getTime()+""));
            put.addColumn(Bytes.toBytes(FAMILY_NAME) , Bytes.toBytes("address") , Bytes.toBytes(record.getAddress()));
            put.addColumn(Bytes.toBytes(FAMILY_NAME) , Bytes.toBytes("longitude") , Bytes.toBytes(record.getLongitude()+""));
            put.addColumn(Bytes.toBytes(FAMILY_NAME) , Bytes.toBytes("latitude") , Bytes.toBytes(record.getLatitude()+""));


            allPuts.add(put);
        }

        //3.执行数据库插入操作
        Table table = HBaseConf.getTableByName(tableName);
        try {
            table.put(allPuts);
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        }
        return true;
    }
}
