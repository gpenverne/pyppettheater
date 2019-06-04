# Pyppettheater

Using puppeteer, docker, and python-gherkin-parser, you can easilly write functionnal tests using gherkin syntax.

## Use as binary script
Install it:
```bash
$ pip3 install Pyppetheater
```

And use it:
```bash
$ pyppet_theater "/path/to/my-yml-or-feature-file"
```

## Use with docker-compose
Just add a service using this image in your ``docker-compose.yml``:
```yaml
tests:
    image: gpenverne/pyppettheater:latest
    volumes:
        - ./tests/scenarios:/scenarios
    working_dir: /
    links:
      - "other-container-name:my-site.com"
      - "another-container-name:a-sub-domain-website"
    stdin_open: true
    tty: true
```
Adjust the ``volumes`` section as your need, to put your scenario folder in the docker container (in my case, all my scenarios are in a ``/tests/scenarios`` folder)

To run your tests suites, just run
```bash
docker-compose run tests pyppet_theater /scenarios/my-suite.yml
docker-compose run tests pyppet_theater /scenarios/my-features/my-scenario.feature
```

## Writing scenarios
Sample folders tree:
```
| tests
	| scenarios
		my-suite.yml
		| my-features
			my-feature.feature
			my-other-feature.feature
```

``my-suite.yml`` contains a simple "scenarios" sortered array with all your features:
```yaml
scenarios:
    0: my-features/my-feature.feature
    2: my-features/my-other-feature.feature
```
Each ``.feature`` is a gherkin file which contains scenarios about your feature:
```gherkin
Feature: Create an account on a game

	Scenario: As a visitor, I register on the game
		Given I go on "http://my-website.com/"
		And I click on "\#signup-link"
		And I type "player6" in field "\#id_username"
		And I type "somepassword" in field "\#id_password1"
		And I type "somepassword" in field "\#id_password2"
		When I click on "\#content-section form button"
		Then I should be on "http://my-website.com/welcome"

	Scenario: As a new player, my elements has been setted with default values
		Given I go on "http://my-website.com/"
		And I click on "\#module-1"
		Then the element "\#quantity-for-1" should have "2000" as content
		And the element "\#quantity-for-2" should have "1000" as content
		And the element "\#quantity-for-3" should have "1000" as content
```

## About actors
An actor is a python class which handle sentences. By default the ``Dom`` actor is loaded which can handle these sentences:

### DOM - navigation
- I go on "http://myurl"
- Take a screenshot
- I should be on "http://myurl"
- I type "something" in field "#query"
- I click on "#item"
- The element "#element" should have "some content" as content
- The element "#element" should not exists
- The element "#element" should exists
-
### MySQL
#### Configuration
```yaml
parameters:
    mysql:
        db_host: db
        db_user: root
        db_password: root
        db_name: test

scenarios:
    0: "mysql/mysql-suite.feature"
```
#### Usage
- The row with ":key" equal to ":value" in table ":table:" should exist
- The row with ":key" equal to ":value" in table ":table:" should not exist
- The row with ":key" equal to ":value" in table ":table:" has ":other_key" equal to ":new_value"
- The row with ":key" equal to ":value" in table ":table:" does not exist
- Then the row with ":key" equal to ":value" in table ":table:" should have ":other_key" equal to ":new_value"

### Rest API
#### Configuration
```yaml
parameters:
    rest:
        base_endpoint: https://my-api-endpoint.com

scenarios:
    0: rest/rest-suite.feature

```
#### Usage
- I add these headers
- I prepare a "GET|POST" request to "url" with data
- I prepare a "GET" request to "url"
- I send the request
- Print the last response
- Print the last json response
- The json node "aaaa" should exist
- The json node "aaaa" should not exist
- The json node "id" should be equal to "1"
- Then the JSON node "" should have "500" elements
- Then the response status code should be "200"
- Then the response content-type should be "application/json; charset=utf-8"
- And the json nodes should be equal to:

If you need or want other sentences, open an issue or create a custom actor :)

To load custom actors, you can add a "Actors" section in your yml file, with all relatives paths (relative to the yaml file) to your actors classes:
```yaml
actors:
    - "../actors/custom_actor.py"
```

## Known limitations
- Each feature is session independant: if you are logged in one .feature, you will not be logged in another one
- Because of gherkin comments, you have to escape ``#`` selectors with a ``\``

## Sample scenarios and yml files
(Tests on this repo)[https://github.com/gpenverne/pyppettheater/tree/master/tests/]

## Contexts & faker
Using (faker)[https://faker.readthedocs.io/en/latest/providers/faker.providers.automotive.html], you can generate (and set) fake generated values in your tests. For example:
```gherkin
	Scenario: We can send POST data using fake generated values
 		Given I prepare a "POST" request to "/posts" with data:
			| title  | <title:faker.name> |
			| body   | bar			      |
			| userId | 1			      |
		When I send the request
		Then the JSON node "title" should be equal to "<context.title>"
```

In this exemple, we send data, with a random generated name as title. The syntax ``<var_name:faker.method>`` means you can retrieve the value using the context: ``<context.title>``
