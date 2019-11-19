package edu.xidian.sselab.cloudcourse.controller;

import edu.xidian.sselab.cloudcourse.domain.Meet;
import edu.xidian.sselab.cloudcourse.domain.Record;
import edu.xidian.sselab.cloudcourse.domain.Track;
import edu.xidian.sselab.cloudcourse.domain.TrackRequest;
import edu.xidian.sselab.cloudcourse.repository.MeetRepository;
import edu.xidian.sselab.cloudcourse.repository.TrackRepository;
import groovy.lang.Tuple2;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.List;

@Controller
@RequestMapping("/meet")
public class MeetController {
    private final MeetRepository repository;

    @Autowired
    public MeetController(MeetRepository repository) {
        this.repository = repository;
    }

    @GetMapping("")
    public String get(Model model) {
        model.addAttribute("title", "相遇统计");
        model.addAttribute("condition", new Record());
        return "meet";
    }

    @PostMapping("")
    public String post(Model model, Record record) {
        Tuple2<List<Meet>, String> meetList = repository.findAllByRecord(record, record.getAddress());
        model.addAttribute("meetList", meetList.getFirst());
        model.addAttribute("startRow", meetList.getSecond());
        model.addAttribute("title", "相遇统计");
        model.addAttribute("condition", record);
        return "meet";
    }
}
