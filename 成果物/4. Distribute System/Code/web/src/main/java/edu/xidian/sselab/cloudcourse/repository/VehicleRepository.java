package edu.xidian.sselab.cloudcourse.repository;

import edu.xidian.sselab.cloudcourse.Constant.Conf;
import edu.xidian.sselab.cloudcourse.domain.Record;
import edu.xidian.sselab.cloudcourse.domain.VehicleCount;
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
public class VehicleRepository {
    private static final String TABLE_NAME = "VehicleCount";


    private final HbaseClient hbaseClient;

    @Autowired
    public VehicleRepository(HbaseClient hbaseClient) {
        this.hbaseClient = hbaseClient;
    }

    public List<VehicleCount> findAll(VehicleCount record) {
        List<VehicleCount> resultRecords = new ArrayList<>();
        hbaseClient.getConnection();
        Table table = hbaseClient.getTableByName(TABLE_NAME);

        FilterList filterList = new FilterList(FilterList.Operator.MUST_PASS_ALL);

        if (record.getPlaceId() != null) {
            RowFilter rowFilter = new RowFilter(
                    CompareFilter.CompareOp.EQUAL,
                    new RegexStringComparator(record.getPlaceId().toString()));
            filterList.addFilter(rowFilter);
        }

        Scan scan = new Scan();
        if (filterList.getFilters().size() != 0) {
            scan.setFilter(filterList);
        }

        ResultScanner rs;

//        int cnt = 0;
//        String newStartRow = "end";
        try {
            if (table != null) {
                rs = table.getScanner(scan);
                for (Result result : rs) {
//                    if (cnt == Conf.PAGE_SIZE) {
//                        newStartRow = Bytes.toString(result.getRow());
//                        break;
//                    }
//                    cnt++;

                    VehicleCount tempRecord = new VehicleCount().mapFrom(result);
                    resultRecords.add(tempRecord);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
            System.out.println("查询出错，返回一个空的列表!");
        }

        return resultRecords;
    }
}
