package edu.xidian.sselab.cloudcourse.controller;

import edu.xidian.sselab.cloudcourse.domain.Record;
import edu.xidian.sselab.cloudcourse.repository.InvalidRepository;
import edu.xidian.sselab.cloudcourse.repository.RecordRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.List;

@Controller
@RequestMapping("/invalid")
public class InvalidController {
    private final InvalidRepository repository;

    @Autowired
    public InvalidController(InvalidRepository repository) {
        this.repository = repository;
    }

    @GetMapping("")
    public String get(Model model) {
        List<Record> recordList = repository.findAll();
        model.addAttribute("title", "无效记录");
        model.addAttribute("recordList", recordList);
        return "invalid";
    }
}
