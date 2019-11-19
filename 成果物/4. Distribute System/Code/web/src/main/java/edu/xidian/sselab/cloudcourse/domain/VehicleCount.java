package edu.xidian.sselab.cloudcourse.domain;

import lombok.Data;
import lombok.ToString;
import org.apache.hadoop.hbase.Cell;
import org.apache.hadoop.hbase.CellUtil;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.util.Bytes;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;

@Data
@ToString
public class VehicleCount {
    private Integer placeId;

    private String address;

    private Double longitude;

    private Double latitude;

    private Integer count;

    public VehicleCount mapFrom(Result result) {
        // 1.分解行键
        setPlaceId(Integer.parseInt(Bytes.toString(result.getRow())));
        // 2.解析所有的列信息
        List<Cell> cellList =  result.listCells();
        for (Cell cell : cellList) {
            String qualifier = Bytes.toString(CellUtil.cloneQualifier(cell));
            String value = Bytes.toString(CellUtil.cloneValue(cell));
            switch (qualifier) {
                case "address": setAddress(value); break;
                case "longitude": setLongitude(Double.parseDouble(value)); break;
                case "latitude": setLatitude(Double.parseDouble(value)); break;
                case "count": setCount(Integer.parseInt(value)); break;
            }
        }

        return this;
    }
}
