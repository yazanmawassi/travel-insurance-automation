package de.viadee.bpm.camunda.travelinsuranceprocessapp.model;

import static de.viadee.bpm.camunda.travelinsuranceprocessapp.TravelInsuranceProcessAppApplication.TRAVEL_INSURANCE_PROCESS_ID;

public class TravelInsuranceProcessException extends RuntimeException {
    public TravelInsuranceProcessException(final Exception cause) {
        super("Unexpected error in process [" + TRAVEL_INSURANCE_PROCESS_ID + "]", cause);
    }
}
