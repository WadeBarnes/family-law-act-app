import { ApplicationState, RootState } from "@/models/storeState";
import { ActionTree } from "vuex";

export const actions: ActionTree<ApplicationState, RootState> = {
  init(context) {
    context.commit("init");
  },
  setUserType(context, userType) {
    context.commit("setUserType", userType);
  },
  setCurrentStep(context, currentStep) {
    context.commit("setCurrentStep", currentStep);
  },
  setCurrentStepPage(context, { currentStep, currentPage }) {
    context.commit("setCurrentStepPage", { currentStep, currentPage });
  },
  setUserName(context, userName) {
    context.commit("setUserName", userName);
  },
  setStepActive(context, { currentStep, active }) {
    context.commit("setStepActive", { currentStep, active });
  },
  gotoPrevStepPage(context) {
    const prevStepPage = context.getters["getPrevStepPage"];

    if (prevStepPage != null) {
      context.commit("gotoPrevStepPage", prevStepPage);
    }
  },
  gotoNextStepPage(context) {
    const nextStepPage = context.getters["getNextStepPage"];

    if (nextStepPage != null) {
      context.commit("gotoNextStepPage", nextStepPage);
    }
  },
  setSelectedForms(context, selectedForms) {
    context.commit("setSelectedForms", selectedForms);
  },
  setApplicantName(context, applicantName) {
    context.commit("setApplicantName", applicantName);
  },
  setYourInformationSurvey(context, yourInformationSurvey) {
    context.commit("setYourInformationSurvey", yourInformationSurvey);
  },
  setPageActive(context, { currentStep, currentPage, active }) {
    context.commit("setPageActive", { currentStep, currentPage, active });
  },
  setOtherParties(context, otherParties) {
    context.commit("setOtherParties", otherParties);
  },
  setSelectedPOOrder(context, selectedPOOrder) {
    context.commit("setSelectedPOOrder", selectedPOOrder);
  },
  setUrgencySurvey(context, urgencySurvey) {
    context.commit("setUrgencySurvey", urgencySurvey);
  },
  setAboutPOSurvey(context, aboutPOSurvey) {
    context.commit("setAboutPOSurvey", aboutPOSurvey);
  }
};
