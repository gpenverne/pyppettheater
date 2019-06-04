Feature: Use the rest test suite

	Scenario: We can fetch data from an api
		Given I add these headers:
			| accept | application/json |
		Given I prepare a "GET" request to "/todos/1"
		When I send the request
		Then print the last json response
		And the json node "anythng" should not exist
		And the json node "userId" should exist
		And the json node "id" should be equal to "1"
		And the response status code should be "200"
		And the response content-type should be "application/json; charset=utf-8"
		And the json nodes should be equal to:
			| id	 | 1 |
			| userId | 1 |

	Scenario: We can count number of items in an array
		Given I add these headers:
			| accept | application/json |
		Given I prepare a "GET" request to "/comments"
		When I send the request
		Then the JSON node "" should have "500" elements
		And the JSON node "[0].id" should be equal to "1"
		And the JSON node "[0].postId" should exist
		And the JSON node "[0].anything" should not exist

	Scenario: We can send POST data
 		Given I prepare a "POST" request to "/posts" with data:
			| title  | pyppetheater |
			| body   | bar			|
			| userId | 1			|
		When I send the request
		Then the JSON node "title" should be equal to "pyppetheater"

    Scenario Outline: We can use scenario outlines
		Given I prepare a "<method>" request to "<uri>"
        When I send the request
        Then the response content-type should be "application/json; charset=utf-8"
        Examples:
            | method | uri       |
            | GET    | /comments |
            | GET    | /posts    |
