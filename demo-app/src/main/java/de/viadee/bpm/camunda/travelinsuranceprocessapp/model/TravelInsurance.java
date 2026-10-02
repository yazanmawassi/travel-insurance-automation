package de.viadee.bpm.camunda.travelinsuranceprocessapp.model;

import org.apache.commons.lang3.builder.ReflectionToStringBuilder;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

import static org.apache.commons.lang3.builder.ToStringStyle.NO_CLASS_NAME_STYLE;

public class TravelInsurance {

    private TravelData travelData;
    private Partner policyHolder;
    private List<Partner> insuredPartners;
    private boolean baggageInsurance;
    private boolean travelCancellation;

    public TravelData getTravelData() {
        return travelData;
    }

    public void setTravelData(final TravelData travelData) {
        this.travelData = travelData;
    }

    public Partner getPolicyHolder() {
        return policyHolder;
    }

    public void setPolicyHolder(final Partner policyHolder) {
        this.policyHolder = policyHolder;
    }

    public List<Partner> getInsuredPartners() {
        if (Objects.isNull(insuredPartners)) {
            insuredPartners = new ArrayList<>();
        }
        return insuredPartners;
    }

    public void setInsuredPartners(final List<Partner> insuredPartners) {
        this.insuredPartners = insuredPartners;
    }

    public boolean isBaggageInsurance() {
        return baggageInsurance;
    }

    public void setBaggageInsurance(final boolean baggageInsurance) {
        this.baggageInsurance = baggageInsurance;
    }

    public boolean isTravelCancellation() {
        return travelCancellation;
    }

    public void setTravelCancellation(final boolean travelCancellation) {
        this.travelCancellation = travelCancellation;
    }

    @Override
    public String toString() {
        return ReflectionToStringBuilder.toString(this, NO_CLASS_NAME_STYLE, false, false, true, Object.class);
    }
}
