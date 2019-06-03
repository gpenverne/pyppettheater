Feature: Use the mysql test suite

	Scenario: We can select, update and check existence
		Given the row with "id" equal to "1" in table "some_table" should exist
		And the row with "id" equal to "1" in table "some_table" has "some_key" equal to "some_value"
		Then the row with "id" equal to "1" in table "some_table" should have "some_key" equal to "some_value"
		And the row with "some_key" equal to "some_value" in table "some_table" should exist

	Scenario: We can delete and check existence
		Given the row with "id" equal to "1" in table "some_table" does not exist
		Then the row with "id" equal to "1" in table "some_table" should not exist
