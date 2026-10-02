package de.viadee.bpm.camunda.travelinsuranceprocessapp.processinterface;

import de.viadee.bpm.camunda.travelinsuranceprocessapp.model.TravelInsuranceRequest;
import de.viadee.bpm.camunda.travelinsuranceprocessapp.service.TravelInsuranceService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class InsuranceRestController {
    private static final Logger log = LoggerFactory.getLogger(InsuranceRestController.class);

    private final TravelInsuranceService travelInsuranceService;

    public InsuranceRestController(final TravelInsuranceService travelInsuranceService) {
        this.travelInsuranceService = travelInsuranceService;
    }

    @PostMapping(value = "/api/travel-insurance", consumes = "application/json")
    public String travelInsuranceRest(@RequestBody final TravelInsuranceRequest travelInsuranceRequest) {
        log.info("Incoming travel-insurance-request: {}", travelInsuranceRequest);
        var processInstanceKey = travelInsuranceService.startTravelInsuranceProcess(travelInsuranceRequest);
        return String.format("{\"processInstanceKey\": %s}", processInstanceKey);
    }

}
