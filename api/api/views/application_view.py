import json
import logging
from django.conf import settings
from django.http import (
    HttpResponseBadRequest,
    HttpResponseNotFound, HttpResponseForbidden
)
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from api.models import Application, EFilingSubmission
from api.utils import get_application_for_user

LOGGER = logging.getLogger(__name__)


class ApplicationView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def encrypt_steps(self, steps):
        try:
            steps_bin = json.dumps(steps).encode("ascii")
            (steps_key_id, steps_enc) = settings.ENCRYPTOR.encrypt(steps_bin)
            return (steps_key_id, steps_enc)
        except Exception as ex:
            LOGGER.error("ERROR! %s", ex)

    def get(self, request, pk, format=None):
        uid = request.user.id
        application = get_application_for_user(pk, uid)
        steps_dec = settings.ENCRYPTOR.decrypt(application.key_id, application.steps)
        steps = json.loads(steps_dec)
        submission = EFilingSubmission.objects.filter(
            id=application.last_efiling_submission_id
        ).first()
        data = {"id": application.id,
                "type": application.app_type,
                "steps": steps,
                "lastUpdate": application.last_updated,
                "lastPrinted": application.last_printed,
                "currentStep": application.current_step,
                "allCompleted": application.all_completed,
                "userType": application.user_type,
                "userName": application.user_name,
                "userId": application.user_id,
                "applicantName": application.applicant_name,
                "respondentName": application.respondent_name,
                "protectedPartyName": application.protected_party_name,
                "protectedChildName": application.protected_child_name,
                "applicationLocation": application.application_location,
                "packageNumber": submission.package_number if submission is not None else "",
                "packageUrl": submission.package_url if submission is not None else "",
                "lastFiled": application.last_filed}
        return Response(data)

    def post(self, request: Request):
        uid = request.user.id
        if not uid:
            return HttpResponseForbidden("Missing user ID")

        body = request.data
        if not body:
            return HttpResponseBadRequest("Missing request body")

        (steps_key_id, steps_enc) = self.encrypt_steps(body["steps"])

        db_app = Application(
            last_updated=body.get("lastUpdate"),
            last_printed=body.get("lastPrinted"),
            app_type=body.get("type"),
            current_step=body.get("currentStep"),
            all_completed=body.get("allCompleted"),
            steps=steps_enc,
            user_type=body.get("userType"),
            applicant_name=body.get("applicantName"),
            user_name=body.get("userName"),
            key_id=steps_key_id,
            respondent_name=body.get("respondentName"),
            protected_party_name=body.get("protectedPartyName"),
            protected_child_name=body.get("protectedChildName"),
            application_location=body.get("applicationLocation"),
            user_id=uid)

        db_app.save()
        return Response({"app_id": db_app.pk})

    def put(self, request, pk, format=None):
        uid = request.user.id
        body = request.data
        if not body:
            return HttpResponseBadRequest("Missing request body")

        app = get_application_for_user(pk, uid)
        if not app:
            return HttpResponseNotFound("No record found")

        (steps_key_id, steps_enc) = self.encrypt_steps(body["steps"])

        app.last_updated = timezone.now()
        app.app_type = body.get("type")
        app.current_step = body.get("currentStep")
        app.steps = steps_enc
        app.user_type = body.get("userType")
        app.applicant_name = body.get("applicantName")
        app.user_name = body.get("userName")
        app.respondent_name = body.get("respondentName")
        app.protected_party_name = body.get("protectedPartyName")
        app.protected_child_name = body.get("protectedChildName")
        app.application_location = body.get("applicationLocation")
        app.save()

        return Response("success")

    def delete(self, request, pk, format=None):
        uid = request.user.id
        application = get_application_for_user(pk, uid)
        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
