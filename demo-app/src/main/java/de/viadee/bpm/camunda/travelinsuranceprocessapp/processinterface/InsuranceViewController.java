package de.viadee.bpm.camunda.travelinsuranceprocessapp.processinterface;

import de.viadee.bpm.camunda.travelinsuranceprocessapp.model.Partner;
import de.viadee.bpm.camunda.travelinsuranceprocessapp.model.TravelData;
import de.viadee.bpm.camunda.travelinsuranceprocessapp.model.TravelInsurance;
import de.viadee.bpm.camunda.travelinsuranceprocessapp.model.TravelInsuranceRequest;
import de.viadee.bpm.camunda.travelinsuranceprocessapp.service.TravelInsuranceService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.ArrayList;

@Controller
public class InsuranceViewController {
    private static final Logger log = LoggerFactory.getLogger(InsuranceViewController.class);

    private final TravelInsuranceService travelInsuranceService;

    public InsuranceViewController(final TravelInsuranceService travelInsuranceService) {
        this.travelInsuranceService = travelInsuranceService;
    }

    @GetMapping("/")
    public String createTravelInsurance(final Model model) {
        var data = new TravelInsuranceRequest();
        data.setTravelInsurance(new TravelInsurance());
        data.getTravelInsurance().setInsuredPartners(new ArrayList<>());
        data.getTravelInsurance().setTravelData(new TravelData());
        model.addAttribute("travelInsuranceRequest", data);
        model.addAttribute("nextPartner", new Partner());
        return "insurance";
    }

    @RequestMapping(value = "/travel-insurance", params = "addPerson")
    public String addPerson(final Model model,
                            @ModelAttribute final TravelInsuranceRequest travelInsuranceRequest,
                            @ModelAttribute final Partner nextPartner) {
        travelInsuranceRequest.getTravelInsurance().getInsuredPartners().add(nextPartner);
        model.addAttribute("travelInsuranceRequest", travelInsuranceRequest);
        model.addAttribute("nextPartner", new Partner()); // reset
        return "insurance";
    }

    @RequestMapping(value = "/travel-insurance")
    public String travelInsuranceView(final Model model, final TravelInsuranceRequest travelInsuranceRequest) {
        log.info("Incoming travel-insurance-request: {}", travelInsuranceRequest);
        var processInstanceKey = travelInsuranceService.startTravelInsuranceProcess(travelInsuranceRequest);
        model.addAttribute("travelInsuranceRequest", travelInsuranceRequest);
        model.addAttribute("processInstanceKey", processInstanceKey);
        return "complete";
    }

}
