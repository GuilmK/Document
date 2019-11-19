package edu.xidian.sselab.cloudcourse.controller;

import edu.xidian.sselab.cloudcourse.domain.Record;
import edu.xidian.sselab.cloudcourse.domain.Track;
import edu.xidian.sselab.cloudcourse.domain.TrackRequest;
import edu.xidian.sselab.cloudcourse.repository.TrackRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.List;

@Controller
@RequestMapping("/track")
public class TrackController {

    private final TrackRepository repository;

    @Autowired
    public TrackController(TrackRepository repository) {
        this.repository = repository;
    }

    @GetMapping("")
    public String track(Model model) {
        model.addAttribute("title", "轨迹重现");
        model.addAttribute("condition", new TrackRequest());
        return "track";
    }

    @PostMapping("")
    public String trackFilter(Model model, TrackRequest trackRequest) {
        List<Track> trackList = repository.findAllByTrackRequest(trackRequest);
        model.addAttribute("trackList", trackList);
        model.addAttribute("title", "轨迹重现");
        model.addAttribute("condition", trackRequest);
        return "track";
    }
    
}
