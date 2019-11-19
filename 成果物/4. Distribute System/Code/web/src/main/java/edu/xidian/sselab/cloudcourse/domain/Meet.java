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
public class Meet {
    private String meid;
    private String oeid;
    private Integer count;

    public Meet mapFrom(Result result) {
        String[] rowKeys = Bytes.toString(result.getRow()).split("##");
        setMeid(rowKeys[0]);
        // 2.解析所有的列信息
        List<Cell> cellList =  result.listCells();
        for (Cell cell : cellList) {
            String qualifier = Bytes.toString(CellUtil.cloneQualifier(cell));
            String value = Bytes.toString(CellUtil.cloneValue(cell));
            switch (qualifier) {
                case "oeid": setOeid(value); break;
                case "count": setCount(Integer.valueOf(value)); break;
            }
        }

        return this;
    }
}
