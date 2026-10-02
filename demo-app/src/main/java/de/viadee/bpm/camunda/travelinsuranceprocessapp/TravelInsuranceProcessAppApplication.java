package de.viadee.bpm.camunda.travelinsuranceprocessapp;

import io.camunda.client.annotation.Deployment;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;


@SpringBootApplication
// @Deployment(resources = "classpath*:/process/**/*.bpmn")
public class TravelInsuranceProcessAppApplication {
	public static final String TRAVEL_INSURANCE_PROCESS_ID = "Process_qcnnxpc";

	public static void main(String[] args) {
		SpringApplication.run(TravelInsuranceProcessAppApplication.class, args);
	}

}
