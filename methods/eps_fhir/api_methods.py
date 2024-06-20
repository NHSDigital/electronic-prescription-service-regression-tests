import json
import uuid

from features.environment import CIS2_USERS
from messages.eps_fhir.dispense_notification import DispenseNotification
from messages.eps_fhir.prescription import Prescription
from methods.eps_fhir.api_request_body_generators import (
    create_fhir_parameter,
    generate_provenance,
    generate_agent,
    generate_owner,
    generate_group_identifier,
    generate_return,
)
from methods.shared.common import the_expected_response_code_is_returned
from methods.shared.api import post, get_headers
from utils.signing import get_signature


def _cancel_medication_request(medication_request):
    medication_request["resource"]["status"] = "cancelled"
    medication_request["resource"]["statusReason"] = {
        "coding": [
            {
                "system": "https://fhir.nhs.uk/CodeSystem/medicationrequest-status-reason",
                "code": "0001",
                "display": "Prescribing Error",
            }
        ]
    }


def _create_cancel_body(context):
    cancel_body = json.loads(context.prepare_body)

    medication_requests = [
        e
        for e in cancel_body["entry"]
        if e["resource"]["resourceType"] == "MedicationRequest"
    ]
    [_cancel_medication_request(mr) for mr in medication_requests]

    message_header = [
        e
        for e in cancel_body["entry"]
        if e["resource"]["resourceType"] == "MessageHeader"
    ][0]
    event_coding = message_header["resource"]["eventCoding"]
    event_coding["code"] = "prescription-order-update"
    event_coding["display"] = "Prescription Order Update"

    return json.dumps(cancel_body)


def _replace_ids(body):
    old_id = json.loads(body)["id"]
    return body.replace(old_id, str(uuid.uuid4()))


def prepare_prescription(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/$prepare"
    additional_headers = {"Content-Type": "application/json"}
    headers = get_headers(context, additional_headers)

    context.prepare_body = Prescription(context).body
    response = post(
        data=context.prepare_body, url=url, context=context, headers=headers
    )
    the_expected_response_code_is_returned(context, 200)

    context.digest = response.json()["parameter"][0]["valueString"]
    context.timestamp = response.json()["parameter"][1]["valueString"]


def _create_signed_body(context):
    context.signature = get_signature(digest=context.digest)
    body = json.loads(context.prepare_body)
    provenance = generate_provenance(
        signature=context.signature, timestamp=context.timestamp
    )
    body["entry"].append(provenance)
    body = json.dumps(body)
    return body


def create_signed_prescription(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/$process-message#prescription-order"
    headers = get_headers(context)

    context.signed_body = _create_signed_body(context)
    post(data=context.signed_body, url=url, context=context, headers=headers)
    the_expected_response_code_is_returned(context, 200)


def _create_release_body(context):
    prescription_order_number = context.prescription_id
    group_identifier = generate_group_identifier(
        prescription_order_number=prescription_order_number
    )
    owner = generate_owner(receiver_ods_code=context.receiver_ods_code)
    agent = generate_agent()
    body = create_fhir_parameter(group_identifier, owner, agent)
    return body


def _create_return_body(context):
    short_prescription_id = context.prescription_id
    nhs_number = context.nhs_number

    body = generate_return(nhs_number, short_prescription_id)
    return json.dumps(body)


def release_signed_prescription(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/Task/$release"
    additional_headers = {"NHSD-Session-URID": CIS2_USERS["dispenser"]["role_id"]}
    headers = get_headers(context, additional_headers)

    context.release_body = _create_release_body(context)
    post(data=context.release_body, url=url, context=context, headers=headers)


def cancel_all_line_items(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/$process-message"
    additional_headers = {"NHSD-Session-URID": CIS2_USERS["prescriber"]["role_id"]}
    headers = get_headers(context, additional_headers)

    cancel_body = _create_cancel_body(context)
    cancel_body = _replace_ids(cancel_body)
    context.cancel_body = cancel_body

    post(data=cancel_body, url=url, context=context, headers=headers)


def dispense_prescription(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/$process-message#dispense-notification"
    additional_headers = {"NHSD-Session-URID": CIS2_USERS["dispenser"]["role_id"]}
    headers = get_headers(context, additional_headers)

    dispense_notification = DispenseNotification(context)

    post(data=dispense_notification.body, url=url, context=context, headers=headers)


def return_prescription(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/Task"
    additional_headers = {"NHSD-Session-URID": CIS2_USERS["dispenser"]["role_id"]}
    headers = get_headers(context, additional_headers)

    context.return_body = _create_return_body(context)
    post(data=context.return_body, url=url, context=context, headers=headers)


def assert_ok_status_code(context):
    the_expected_response_code_is_returned(context, 200)
