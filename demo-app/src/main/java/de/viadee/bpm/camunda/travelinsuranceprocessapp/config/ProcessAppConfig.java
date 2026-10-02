package de.viadee.bpm.camunda.travelinsuranceprocessapp.config;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.databind.json.JsonMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import static com.fasterxml.jackson.databind.SerializationFeature.WRITE_DATES_AS_TIMESTAMPS;

@Configuration
public class ProcessAppConfig {

    @Bean
    public JsonMapper jsonMapper() {
        var jsonMapper = new JsonMapper();
        jsonMapper.registerModule(new JavaTimeModule());
        jsonMapper.disable(WRITE_DATES_AS_TIMESTAMPS);
        jsonMapper.setDefaultPropertyInclusion(JsonInclude.Include.NON_NULL);
        return jsonMapper;
    }

}
