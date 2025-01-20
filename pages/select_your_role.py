from playwright.sync_api import Page


class SelectYourRole:
    def __init__(self, page: Page):
        """
        Initialise the SelectYourRole page object with locators and text constants.
        """
        self.page = page

        # Title and summary locators
        self.summary = page.locator("summary")
        self.organisation_column_header = page.get_by_role(
            "columnheader", name="Organisation"
        )
        self.role_column_header = page.get_by_role("columnheader", name="Role")

        # Logged-in message
        self.logged_in_message_container = page.get_by_text(
            "Information: Information: You"
        )
        self.logged_in_message = page.get_by_text("You are currently logged in")

        # Roles without access
        self.roles_without_access_table_body = page.get_by_role("group").locator("div")

        self.first_row_org_name = page.get_by_test_id("change-role-name-cell").first
        self.first_row_role_name = page.get_by_test_id("change-role-role-cell").first

        # Role cards - roles with access
        self.roles_with_access_cards = page.locator(".nhsuk-card--clickable")
        self.first_role_card = self.roles_with_access_cards.first
        self.role_card_headings = page.locator(".nhsuk-card__heading")
        self.role_card_descriptions = page.locator(".eps-card__roleName")
        self.selected_role_url = "**/site/yourselectedrole"

        self.select_role_header = page.locator(
            "span[data-testid='eps_header_selectYourRole'] > span.nhsuk-title"
        )
        self.select_role_subheader = page.locator(
            "span.nhsuk-caption-l.nhsuk-caption--bottom"
        )

        self.no_access_header = page.locator(".nhsuk-heading-xl")
        self.no_access_message = page.get_by_text("None of the roles on your")
        self.roles_without_access_header = page.get_by_role(
            "heading", name="Your roles without access"
        )
        self.first_row_org_name_no_access = page.get_by_role(
            "cell", name="NO ORG NAME (ODS: A21464)"
        ).first
        self.first_row_role_name_no_access = page.get_by_role(
            "cell", name="General Medical Practitioner"
        ).first
