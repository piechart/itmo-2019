Feature: Order pizza(s)
  As a user
  I want to order pizza

  Scenario: User chooses one or more pizzas and presses 'Order'
    Given that the user has entered his email address
    When the user chooses one or more pizzas and presses 'Order'
    Then an Order is created in the database
    And a confirmation is sent to the user's email address
