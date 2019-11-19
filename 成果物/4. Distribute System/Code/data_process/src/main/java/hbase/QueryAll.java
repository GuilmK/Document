package hbase;

import data.Record;
import org.apache.hadoop.hbase.Cell;
import org.apache.hadoop.hbase.CellUtil;
import org.apache.hadoop.hbase.client.*;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;


public class QueryAll {

    public List<Record> QueryAll(String tableName) { 
        List<Record> AllRecords =  new ArrayList<Record>();
        RecordMap rm = new RecordMap();
        Table table = HBaseConf.getTableByName("Record");

        try { 
            ResultScanner rs = table.getScanner(new Scan());
            for (Result r : rs) { 
                AllRecords.add(rm.resultMapToRecord(r));
//                System.out.println(rm.resultMapToRecord(r));
            } 
        } catch (IOException e) {
            e.printStackTrace(); 
        } 

        return AllRecords;
    } 


    public static void main(String[] args) {
        QueryAll que = new QueryAll();
        new NewHBaseInsert().insertRecordsToHBase(que.QueryAll("Track"));
    }
}