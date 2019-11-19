package edu.xidian.sselab.cloudcourse.controller;

import edu.xidian.sselab.cloudcourse.domain.VehicleCount;
import edu.xidian.sselab.cloudcourse.repository.VehicleRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.List;

@Controller
@RequestMapping("/vehicle")
public class VehicleController {
    private final VehicleRepository repository;

    @Autowired
    public VehicleController(VehicleRepository repository) {
        this.repository = repository;
    }

    @GetMapping("")
    public String get(Model model) {
        model.addAttribute("title", "地点过车统计");
        model.addAttribute("condition", new VehicleCount());
        model.addAttribute("startRow", "");
        return "vehicle";
    }

    @PostMapping("")
    public String post(Model model, VehicleCount record) {
        List<VehicleCount> response = repository.findAll(record);
        model.addAttribute("recordList", response);
        model.addAttribute("title", "地点过车统计");
        model.addAttribute("condition", record);
        return "vehicle";
    }

}
