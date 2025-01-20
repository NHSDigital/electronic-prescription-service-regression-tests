@cpts_ui @select_your_role @regression @blocker @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
Feature: Role selection page renders roles properly when logged in

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
    Scenario: User can navigate to the select your role page
        Given I am logged in
        And I go to the select your role page

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4656
    Scenario: User is redirected to the select your role page
        Given I am logged in
        And I go to the select your role page

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
    Scenario: User can see the summary container, but not the table contents by default
        Given I am logged in
        And I go to the select your role page
        Then I can see the summary container
        And I cannot see the summary table body

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
    Scenario: User can expand the summary table to see the contents. Clicking again hides it
        Given I am logged in
        And I go to the select your role page
        When I click on the summary expander
        Then I can see the summary table body
        And I can see the table body has a header row
        And I can see the table body has data
        When I click on the summary expander
        Then I can see the summary container
        And I cannot see the summary table body

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4651
    Scenario: User can see roles with access cards
        Given I am logged in
        And I go to the select your role page
        Then I can see the roles with access cards

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4651
    Scenario: User can navigate to the your selected role page
        Given I am logged in
        And I go to the select your role page
        Then I can navigate to the your selected role page by clicking a card

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4655
    Scenario: User without access can see the header on the select your role page
        Given I am logged in without access
        And I go to the select your role page
        Then I cannot see the your selected role subheader
        And I can see the no access header

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4655
    Scenario: User without access can see the message on the select your role page
        Given I am logged in without access
        And I go to the select your role page
        Then I cannot see the your selected role subheader
        And I can see the no access message

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4655
    Scenario: User without access can see the summary container, but not the table contents by default
        Given I am logged in without access
        And I go to the select your role page
        Then I can see the summary container
        And I cannot see the summary table body

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4655
    Scenario: User without access can expand the summary table to see the contents. Clicking again hides it
        Given I am logged in without access
        And I go to the select your role page
        When I click on the summary expander
        Then I can see the summary table body
        And I can see the table body has a header row
        And I can see the no access table body has data
        When I click on the summary expander
        Then I can see the summary container
        And I cannot see the summary table body

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4645
    Scenario: User with assigned roles sees the correct logged-in message
        Given I am logged in as a user with the role "Health Professional Access Role"
        And I am accessing "GREENE'S PHARMACY (FG419)"
        When I view the homepage
        Then I see a message saying "You are currently logged in at {pharmacy} with {role}."
          | pharmacy               | role                          |
          | GREENE'S PHARMACY (FG419) | Health Professional Access Role |
