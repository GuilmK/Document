package edu.xidian.sselab.cloudcourse.repository;

import edu.xidian.sselab.cloudcourse.Constant.Conf;
import edu.xidian.sselab.cloudcourse.domain.Meet;
import edu.xidian.sselab.cloudcourse.domain.Record;
import edu.xidian.sselab.cloudcourse.hbase.HbaseClient;
import groovy.lang.Tuple2;
import org.apache.commons.lang.StringUtils;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.filter.*;
import org.apache.hadoop.hbase.util.Bytes;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@Component
public class MeetRepository {
    private static final String TABLE_NAME = "MeetCount";

    private static final String FAMILY_NAME = "info";

    private final HbaseClient hbaseClient;

    @Autowired
    public MeetRepository(HbaseClient hbaseClient) {
        this.hbaseClient = hbaseClient;
    }

    public Tuple2<List<Meet>, String> findAllByRecord(Record record, String startRow){
        List<Meet> resultRecords = new ArrayList<>();
        hbaseClient.getConnection();
        Table table = hbaseClient.getTableByName(TABLE_NAME);

        FilterList filterList = new FilterList(FilterList.Operator.MUST_PASS_ALL);

        if (StringUtils.isNotEmpty(record.getEid())) {
            RowFilter rowFilter = new RowFilter(
                    CompareFilter.CompareOp.EQUAL,
                    new RegexStringComparator(record.getEid()+"##"));
            filterList.addFilter(rowFilter);
        }

        Scan scan = new Scan();
        if (filterList.getFilters().size() != 0) {
            scan.setFilter(filterList);
        }
        if (StringUtils.isNotEmpty(startRow)) {
            scan.setStartRow(startRow.getBytes());
        }
        ResultScanner rs;

        int cnt = 0;
        String newStartRow = "end";
        try {
            if (table != null) {
                rs = table.getScanner(scan);
                for (Result result : rs) {
                    if (cnt == Conf.PAGE_SIZE) {
                        newStartRow = Bytes.toString(result.getRow());
                        break;
                    }
                    cnt++;

                    Meet tempRecord = new Meet().mapFrom(result);
                    resultRecords.add(tempRecord);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
            System.out.println("查询出错，返回一个空的列表!");
        }
        return new Tuple2<List<Meet>, String>(resultRecords, newStartRow);
    }
}
