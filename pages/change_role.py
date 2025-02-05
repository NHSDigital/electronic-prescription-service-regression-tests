from playwright.sync_api import Page


class ChangeRole:
    def __init__(self, page: Page):
        """
        Initialise the ChangeRole page object with locators and text constants.
        """
        self.page = page

        # Title and summary locators
        self.change_role_title = page.get_by_text("Change your role")
        self.roles_without_access_table = page.locator("summary")
        self.roles_without_access_organisation_column_header = page.get_by_role(
            "columnheader", name="Organisation"
        )
        self.roles_without_access_role_column_header = page.get_by_role(
            "columnheader", name="Role"
        )
        self.roles_without_access_table_body = page.get_by_role("group").locator("div")
        self.first_row_org_name = page.get_by_test_id("change-role-name-cell").first
        self.first_row_role_name = page.get_by_test_id("change-role-role-cell").first

        # Role cards - roles with access
        self.roles_with_access_cards = page.locator(".nhsuk-card--clickable")
        self.first_role_card = self.roles_with_access_cards.first
        self.role_card_headings = page.locator(".nhsuk-card__heading")
        self.role_card_descriptions = page.locator(".eps-card__roleName")

        # Header locators
        self.select_role_header = page.locator(
            "span[data-testid='eps_header_selectYourRole'] > span.nhsuk-title"
        )
        self.change_role_header = page.get_by_test_id("eps_header_changeRoleLink")

        # Subheader locators
        self.select_role_subheader = page.locator(
            "span.nhsuk-caption-l.nhsuk-caption--bottom"
        )

        self.no_access_title = page.get_by_text("No access to the clinical")
        self.no_access_content = page.get_by_text("None of the roles on your")
