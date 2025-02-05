@cpts_ui @your_selected_role @rbac_banner @regression @blocker @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4537
Feature: When the user selects a role, they see a confirmation page

  Background:
    Given I am logged in

  Scenario: user is able to select a role, and see a confirmation page
    When I go to the select your role page
    And I click a change role role card
    Then I see the 'your selected role' page
    And I can see the RBAC banner

  Scenario: user can change their role, and see a confirmation page
    Given I am on the change your role page
    When I click a change role role card
    Then I see the 'your selected role' page
    And I can see the RBAC banner

  Scenario: user can select a role, then change their mind with the first change link
    Given I am on the your selected role page
    When I click the change link next to the role text
    Then I am on the change role page
    And I can see the RBAC banner

  Scenario: user can select a role, then change their mind with the second change link
    Given I am on the your selected role page
    When I click the change link next to the org text
    Then I am on the change role page
    And I can see the RBAC banner

  Scenario: user is sent from role confirmation page to the search for a prescription page
    Given I am on the your selected role page
    When I click the confirm and continue button on the your selected role page
    Then I am on the search for a prescription page
    And I can see the RBAC banner
