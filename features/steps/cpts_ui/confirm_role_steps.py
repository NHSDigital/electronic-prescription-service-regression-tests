# pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.confirm_role import ConfirmRole


############################################################################
# GIVEN STEPS
############################################################################


@given("I am on the confirm your role page")
def i_am_on_the_confirm_your_role_page(context):
    context.execute_steps("when I have a selected role")
    context.execute_steps("then I see the 'confirm your role' page")


############################################################################
# WHEN STEPS
############################################################################


@when("I click the change link next to the role text")
def i_click_the_change_link_next_to_the_role_text(context):
    confirm_role_page = ConfirmRole(context.page)
    confirm_role_page.role_change_role.click()


@when("I click the change link next to the org text")
def i_click_the_change_link_next_to_the_org_text(context):
    confirm_role_page = ConfirmRole(context.page)
    confirm_role_page.org_change_role.click()


@when("I click the confirm and continue button on the confirm role page")
def i_click_the_confirm_and_continue_button_on_the_confirm_role_page(context):
    confirm_role_page = ConfirmRole(context.page)
    confirm_role_page.confirm_button.click()


############################################################################
# THEN STEPS
############################################################################


@then("I see the 'confirm your role' page")
def i_see_the_confirm_your_role_page(context):
    confirm_role_page = ConfirmRole(context.page)

    expect(confirm_role_page.header).to_be_visible()
    expect(confirm_role_page.role_label_cell).to_be_visible()
    expect(confirm_role_page.org_label_cell).to_be_visible()
    expect(confirm_role_page.org_text_cell).to_be_visible()
    expect(confirm_role_page.role_text_cell).to_be_visible()
    expect(confirm_role_page.role_change_role).to_be_visible()
    expect(confirm_role_page.org_change_role).to_be_visible()
