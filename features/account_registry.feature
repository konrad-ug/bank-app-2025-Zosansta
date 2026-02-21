Feature: Account registry

  Scenario: User is able to create 2 accounts
    Given Account registry is empty
    When I create an account using name: "kurt", last name: "cobain", pesel: "89092909246"
    And I create an account using name: "tadeusz", last name: "szcześniak", pesel: "79101011234"
    Then Number of accounts in registry equals: "2"
    And Account with pesel "89092909246" exists in registry
    And Account with pesel "79101011234" exists in registry

  Scenario: User is able to update surname of already created account
    Given Account registry is empty
    And I create an account using name: "nata", last name: "haydamaky", pesel: "95092909876"
    When I update "surname" of account with pesel: "95092909876" to "filatov"
    Then Account with pesel "95092909876" has "surname" equal to "filatov"

  Scenario: User is able to update name of already created account
    Given Account registry is empty
    And I create an account using name: "kurt", last name: "cobain", pesel: "89092909246"
    When I update "name" of account with pesel: "89092909246" to "frances"
    Then Account with pesel "89092909246" has "name" equal to "frances"

  Scenario: Created account has all fields correctly set
    Given Account registry is empty
    When I create an account using name: "kurt", last name: "cobain", pesel: "89092909246"
    Then Account with pesel "89092909246" has "name" equal to "kurt"
    And Account with pesel "89092909246" has "surname" equal to "cobain"

  Scenario: User is able to delete created account
    Given Account registry is empty
    And I create an account using name: "parov", last name: "stelar", pesel: "01092909876"
    When I delete account with pesel: "01092909876"
    Then Account with pesel "01092909876" does not exist in registry
    And Number of accounts in registry equals: "0"

  Scenario: Successful transfer between two accounts
    Given Account registry is empty
    And I create an account using name: "Jan", last name: "Kowalski", pesel: "11111111111"
    And I create an account using name: "Anna", last name: "Nowak", pesel: "22222222222"
    And Account with pesel "11111111111" has balance: "500"
    When I perform a transfer of "200" from "11111111111" to "22222222222"
    Then Account with pesel "11111111111" has balance equal to "300"
    And Account with pesel "22222222222" has balance equal to "200"