package edu.xidian.sselab.cloudcourse.controller;

import edu.xidian.sselab.cloudcourse.domain.Record;
import edu.xidian.sselab.cloudcourse.repository.RecordRepository;
import groovy.lang.Tuple2;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.List;

@Controller
@RequestMapping("/record")
public class RecordController {
    
    private final RecordRepository repository;

    @Autowired
    public RecordController(RecordRepository repository) {
        this.repository = repository;
    }

    @GetMapping("")
    public String get(Model model) {
        model.addAttribute("title", "过车统计");
        model.addAttribute("condition", new Record());
        model.addAttribute("startRow", "");
        return "record";
    }

    // address 是 startRow
    @PostMapping("")
    public String post(Model model, Record record) {
        Tuple2<List<Record>, String> response = repository.findAllByRecord(record, record.getAddress());
        model.addAttribute("recordList", response.getFirst());
        model.addAttribute("title", "过车统计");
        model.addAttribute("condition", record);
        model.addAttribute("startRow", response.getSecond());
        return "record";
    }
    
}
