package de.viadee.bpm.camunda.travelinsuranceprocessapp.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.json.JsonMapper;
import de.viadee.bpm.camunda.travelinsuranceprocessapp.model.TravelInsuranceProcessException;
import de.viadee.bpm.camunda.travelinsuranceprocessapp.model.TravelInsuranceRequest;
import io.camunda.client.CamundaClient;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import static de.viadee.bpm.camunda.travelinsuranceprocessapp.TravelInsuranceProcessAppApplication.TRAVEL_INSURANCE_PROCESS_ID;

@Service
public class TravelInsuranceService {
    private static final Logger log = LoggerFactory.getLogger(TravelInsuranceService.class);

    private final CamundaClient camundaClient;
    private final JsonMapper jsonMapper;

    public TravelInsuranceService(final CamundaClient camundaClient,
                                  final JsonMapper jsonMapper) {
        this.camundaClient = camundaClient;
        this.jsonMapper = jsonMapper;
    }


    public long startTravelInsuranceProcess(final TravelInsuranceRequest travelInsuranceRequest) {
        log.debug("Start process-instance, using process-id '{}'", TRAVEL_INSURANCE_PROCESS_ID);
        var processInstance = camundaClient.newCreateInstanceCommand()
                                         .bpmnProcessId(TRAVEL_INSURANCE_PROCESS_ID)
                                         .latestVersion()
                                         .variables(this.asJson(travelInsuranceRequest))
                                         .send().join();

        var processInstanceKey = processInstance.getProcessInstanceKey();
        log.info("Process instance started, processInstanceKey: {}", processInstanceKey);
        return processInstanceKey;
    }


    private String asJson(final Object object) {
        try {
            return jsonMapper.writeValueAsString(object);

        } catch (final JsonProcessingException e) {
            log.error("Some error occurred while writing json: {}", e.getMessage());
            throw new TravelInsuranceProcessException(e);
        }
    }

}
