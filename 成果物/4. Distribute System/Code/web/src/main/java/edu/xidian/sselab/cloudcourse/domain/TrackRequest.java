package edu.xidian.sselab.cloudcourse.domain;

import lombok.Data;
import lombok.ToString;

@Data
@ToString
public class TrackRequest {
    private String eid;

    private Long startTime;
    private Long endTime;

}
