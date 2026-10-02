package de.viadee.bpm.camunda.travelinsuranceprocessapp.model;

import org.apache.commons.lang3.builder.ReflectionToStringBuilder;

import static org.apache.commons.lang3.builder.ToStringStyle.NO_CLASS_NAME_STYLE;

public class TravelInsuranceRequest {

    private TravelInsurance travelInsurance;

    public TravelInsurance getTravelInsurance() {
        return travelInsurance;
    }

    public void setTravelInsurance(final TravelInsurance travelInsurance) {
        this.travelInsurance = travelInsurance;
    }

    @Override
    public String toString() {
        return ReflectionToStringBuilder.toString(this, NO_CLASS_NAME_STYLE, false, false, true, Object.class);
    }
}
