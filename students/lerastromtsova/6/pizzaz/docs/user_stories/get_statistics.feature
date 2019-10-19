Feature: Ordered pizzas statistics
  As a delivery service manager
  I want to see statistics about pizzas that were ordered on our website
  So that I am able to analyze it

  Scenario: Manager opens the 'Statistics' tab on our website
    When the manager opens the 'Statistics' tab on our website
    Then full list of pizzas ordered today is displayed
    And it is possible to filter the list by pizza status
    And it is possible to filter the list by pizza name
