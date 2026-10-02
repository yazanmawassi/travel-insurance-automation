package de.viadee.bpm.camunda.travelinsuranceprocessapp.worker;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.json.JsonMapper;
import de.viadee.bpm.camunda.travelinsuranceprocessapp.model.TravelInsuranceProcessException;
import de.viadee.bpm.camunda.travelinsuranceprocessapp.model.TravelInsuranceRequest;
import io.camunda.client.annotation.JobWorker;
import io.camunda.client.api.response.ActivatedJob;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

@Component
public class TravelInsuranceReadInputData {
    private static final Logger log = LoggerFactory.getLogger(TravelInsuranceReadInputData.class);

    private final JsonMapper jsonMapper;

    public TravelInsuranceReadInputData(final JsonMapper jsonMapper) {
        this.jsonMapper = jsonMapper;
    }

    @JobWorker(type = "read-input-data", fetchVariables = {"travelInsurance"})
    public void execute(final ActivatedJob job) {
        log.info("Start 'read-input-data'... ");

        var raw = job.getVariables();
        log.info("input-data [type={}]: {}", raw.getClass().getSimpleName(), raw);

        var inputData = fromJson(raw);
        log.info("input-data [type={}]: {}", inputData.getClass().getSimpleName(), inputData);

    }


    private TravelInsuranceRequest fromJson(final Object jsonData) {
        try {
            return jsonMapper.readValue(String.valueOf(jsonData), TravelInsuranceRequest.class);

        } catch (JsonProcessingException e) {
            log.error("Some error occurred while reading json: {}", e.getMessage());
            throw new TravelInsuranceProcessException(e);
        }
    }

}
