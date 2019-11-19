package edu.xidian.sselab.cloudcourse.domain;

import lombok.Data;
import lombok.ToString;
import org.apache.hadoop.hbase.Cell;
import org.apache.hadoop.hbase.CellUtil;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.util.Bytes;

import java.util.List;

@Data
@ToString
public class Track {
    private String eid;

    private Long time;

    private Integer placeId;

    private String address;

    private Double longitude;

    private Double latitude;

    public Track mapFrom(Result result) {
        String[] rowKey = Bytes.toString(result.getRow()).split("##");
        // 1.分解行键
        setEid(rowKey[0]);
        // 2.解析所有的列信息
        List<Cell> cellList =  result.listCells();
        for (Cell cell : cellList) {
            String qualifier = Bytes.toString(CellUtil.cloneQualifier(cell));
            String value = Bytes.toString(CellUtil.cloneValue(cell));
            switch (qualifier) {
                case "time": setTime(Long.valueOf(value)); break;
                case "placeId": setPlaceId(Integer.valueOf(value)); break;
                case "address": setAddress(value); break;
                case "longitude": setLongitude(Double.parseDouble(value)); break;
                case "latitude": setLatitude(Double.parseDouble(value)); break;
            }
        }

        return this;
    }
}
