# pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from features.environment import (
    MOCK_CIS2_LOGIN_ID_MULTIPLE_ACCESS_ROLES,
    MOCK_CIS2_LOGIN_ID_NO_ACCESS_ROLE,
    MOCK_CIS2_LOGIN_ID_SINGLE_ACCESS_ROLE,
    MOCK_CIS2_LOGIN_ID_MULTIPLE_ACCESS_ROLES_WITH_SELECTED_ROLE,
)

from pages.select_your_role import SelectYourRole

###############################################################################
# GIVEN
###############################################################################


@given("I am on the home page")
def i_am_on_home_page(context):
    context.page.goto(context.cpts_ui_base_url + "site/")


@given("I am on the login page")
def i_am_on_login_page(context):
    context.execute_steps("given I am on the home page")
    context.page.get_by_test_id("eps_header_serviceName").click()


@given("I am logged in")
def login(context):
    context.execute_steps("given I am on the login page")

    context.page.get_by_role("button", name="Log in with mock CIS2").click()
    context.page.get_by_label("Username").fill(MOCK_CIS2_LOGIN_ID_MULTIPLE_ACCESS_ROLES)
    context.page.get_by_role("button", name="Sign In").click()

    select_your_role_page = SelectYourRole(context.page)
    expect(select_your_role_page.page_loaded_indicator).to_be_visible()

    # There should be cookies with names starting with "CognitoIdentityServiceProvider"
    cookies = context.page.context.cookies()
    cognito_cookies = [
        cookie
        for cookie in cookies
        if cookie["name"].startswith("CognitoIdentityServiceProvider")
    ]
    assert len(cognito_cookies) > 0


@given("I am logged in without access")
def login_without_access(context):
    context.execute_steps("given I am on the login page")

    context.page.get_by_role("button", name="Log in with mock CIS2").click()
    context.page.get_by_label("Username").fill(MOCK_CIS2_LOGIN_ID_NO_ACCESS_ROLE)
    context.page.get_by_role("button", name="Sign In").click()


@given("I am logged in with a single access role")
@when("I am logged in with a single access role")
def login_single_role(context):
    context.execute_steps("given I am on the login page")

    context.page.get_by_role("button", name="Log in with mock CIS2").click()
    context.page.get_by_label("Username").fill(MOCK_CIS2_LOGIN_ID_SINGLE_ACCESS_ROLE)
    context.page.get_by_role("button", name="Sign In").click()


@given("I am logged in as a user with a pre selected role")
def login_pre_role_selected(context):
    context.execute_steps("given I am on the login page")
    context.page.get_by_role("button", name="Log in with mock CIS2").click()
    context.page.get_by_label("Username").fill(
        MOCK_CIS2_LOGIN_ID_MULTIPLE_ACCESS_ROLES_WITH_SELECTED_ROLE
    )
    context.page.get_by_role("button", name="Sign In").click()


###############################################################################
# WHEN
###############################################################################


###############################################################################
# THEN STEPS
###############################################################################


@then("I am logged out")
def i_am_logged_out(context):
    # No cookies with names starting with "CognitoIdentityServiceProvider" should be present
    cookies = context.page.context.cookies()
    cognito_cookies = [
        cookie
        for cookie in cookies
        if cookie["name"].startswith("CognitoIdentityServiceProvider")
    ]
    assert len(cognito_cookies) == 0
