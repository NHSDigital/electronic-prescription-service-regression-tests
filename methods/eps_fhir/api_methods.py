import uuid

from methods.eps_fhir.api_request_body_generators import (
    create_fhir_bundle,
    create_fhir_signed_bundle,
    generate_message_header,
    generate_medication_request,
    generate_patient,
    generate_organization,
    generate_practitioner_role,
    generate_practitioner,
    generate_provenance,
)
from methods.shared import common
from methods.shared.api import post, get_default_headers
from utils.prescription_id_generator import generate_short_form_id
from utils.signing import get_signature


def create_new_prepare_body(context):
    # context.bundle_id = uuid.uuid4()
    context.sender_ods_code = "RBA"
    context.prescription_id = generate_short_form_id(ods_code=context.sender_ods_code)
    message_header = generate_message_header(
        bundle_id=uuid.uuid4(), sender_ods_code=context.sender_ods_code
    )
    medication_request = generate_medication_request(
        short_prescription_id=context.prescription_id,
        code=context.nomination_code,
    )
    patient = generate_patient(nhs_number=context.nhs_number)
    organization = generate_organization()
    practitioner_role = generate_practitioner_role()
    practitioner = generate_practitioner()
    body = create_fhir_bundle(
        message_header=message_header,
        medication_request=medication_request,
        patient=patient,
        organization=organization,
        practitioner_role=practitioner_role,
        practitioner=practitioner,
    )
    return body


def prepare_prescription(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/$prepare"
    body = create_new_prepare_body(context)
    headers = get_default_headers()
    headers.update({"Authorization": f"Bearer {context.auth_token}"})
    response = post(data=body, url=url, context=context, headers=headers)
    common.the_expected_response_code_is_returned(context, 200)
    context.digest = response.json()["parameter"][0]["valueString"]


def create_new_digested_body(context):
    context.sender_ods_code = "RBA"
    context.prescription_id = generate_short_form_id(ods_code=context.sender_ods_code)
    context.signature = get_signature(context.digest, True)
    message_header = generate_message_header(
        bundle_id=uuid.uuid4(), sender_ods_code=context.sender_ods_code
    )
    medication_request = generate_medication_request(
        short_prescription_id=context.prescription_id,
        code=context.nomination_code,
    )
    patient = generate_patient(nhs_number=context.nhs_number)
    organization = generate_organization()
    practitioner_role = generate_practitioner_role()
    practitioner = generate_practitioner()
    provenance = generate_provenance(data=context.signature)
    body = create_fhir_signed_bundle(
        message_header=message_header,
        medication_request=medication_request,
        patient=patient,
        organization=organization,
        practitioner_role=practitioner_role,
        practitioner=practitioner,
        provenance=provenance,
    )
    return body


def create_signed_prescription(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/$process-message#prescription-order"
    body = create_new_digested_body(context)
    headers = get_default_headers()
    headers.update({"Authorization": f"Bearer {context.auth_token}"})
    post(data=body, url=url, context=context, headers=headers)
    common.the_expected_response_code_is_returned(context, 200)
