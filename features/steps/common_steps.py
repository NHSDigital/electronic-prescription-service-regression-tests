# pylint: disable=no-name-in-module
from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]
from methods.shared import common
from methods.api.common_api_methods import request_ping
from methods.shared.common import assert_that


@when('I make a request to the "{product}" ping endpoint')
def i_make_a_request_to_the_ping_endpoint(context, product):
    base_url = None
    if product == "pfp_apigee":
        base_url = context.pfp_apigee_base_url
    if product == "eps_fhir":
        base_url = context.eps_fhir_base_url
    if base_url is not None:
        request_ping(context, base_url)
    else:
        raise ValueError(f"unable to find base url for '{product}'")


@then("the response indicates a success")
def indicate_successful_response(context):
    if "sandbox" in context.config.userdata["env"].lower():
        return
    common.the_expected_response_code_is_returned(context, 200)


@then("I can see the version information in the response")
def i_see_version_in_response(context):
    response = context.response.json()
    assert_that(response["version"]).is_not_none()
    assert_that(response["version"]).is_not_empty()


@then("I can see the revision information in the response")
def i_see_revision_in_response(context):
    response = context.response.json()
    assert_that(response["revision"]).is_not_none()
    assert_that(response["revision"]).is_not_empty()


@then("I can see the releaseId information in the response")
def i_see_release_id_in_response(context):
    response = context.response.json()
    assert_that(response["releaseId"]).is_not_none()
    assert_that(response["releaseId"]).is_not_empty()


@then("I can see the commitId information in the response")
def i_see_commit_id_in_response(context):
    response = context.response.json()
    assert_that(response["commitId"]).is_not_none()
    assert_that(response["commitId"]).is_not_empty()


@then("I can see the ping information in the response")
def i_can_see_the_ping_information(context):
    i_see_version_in_response(context)
    i_see_revision_in_response(context)
    i_see_release_id_in_response(context)
    i_see_commit_id_in_response(context)
