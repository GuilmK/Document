package edu.xidian.sselab.cloudcourse.repository;

import edu.xidian.sselab.cloudcourse.domain.Record;
import edu.xidian.sselab.cloudcourse.domain.Track;
import edu.xidian.sselab.cloudcourse.domain.TrackRequest;
import edu.xidian.sselab.cloudcourse.hbase.HbaseClient;
import org.apache.commons.lang.StringUtils;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.filter.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@Component
public class TrackRepository {
    private static final String TABLE_NAME = "Track";

    private static final String FAMILY_NAME = "info";

    private final HbaseClient hbaseClient;

    @Autowired
    public TrackRepository(HbaseClient hbaseClient) {
        this.hbaseClient = hbaseClient;
    }

    public List<Track> findAllByTrackRequest(TrackRequest trackRequest){
        List<Track> resultTrack = new ArrayList<>();
        hbaseClient.getConnection();
        Table table = hbaseClient.getTableByName(TABLE_NAME);

        FilterList filterList = new FilterList(FilterList.Operator.MUST_PASS_ALL);

//        if (trackRequest.getStartTime() != null && trackRequest.getEndTime() != null) {
//            RowFilter startFilter = new RowFilter(
//                    CompareFilter.CompareOp.GREATER_OR_EQUAL,
//                    new BinaryComparator(String.valueOf(trackRequest.getStartTime()).getBytes()));
//            filterList.addFilter(startFilter);
//            RowFilter endFilter = new RowFilter(
//                    CompareFilter.CompareOp.LESS_OR_EQUAL,
//                    new BinaryComparator(String.valueOf(trackRequest.getEndTime()).getBytes()));
//            filterList.addFilter(endFilter);
//        }

        if (StringUtils.isNotEmpty(trackRequest.getEid())) {
            RowFilter rowFilter = new RowFilter(
                    CompareFilter.CompareOp.EQUAL,
                    new SubstringComparator(trackRequest.getEid()));
            filterList.addFilter(rowFilter);
        } else {
            return resultTrack;
        }

        Scan scan = new Scan();
        if (filterList.getFilters().size() != 0) {
            scan.setFilter(filterList);
        }
        if (trackRequest.getStartTime() != null) {
            scan.setStartRow((trackRequest.getEid()+"##"+trackRequest.getStartTime()).getBytes());
        }
        if (trackRequest.getEndTime() != null) {
            scan.setStopRow((trackRequest.getEid()+"##"+trackRequest.getEndTime()).getBytes());
        }

        ResultScanner rs;
        try {
            if (table != null) {
                rs = table.getScanner(scan);
                for (Result result : rs) {
                    Track tempRecord = new Track().mapFrom(result);
                    resultTrack.add(tempRecord);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
            System.out.println("查询出错，返回一个空的列表!");
        }

        return resultTrack;
    }
}
