# Pyppettheater

Using puppeteer, docker, and python-gherkin-parser, you can easilly write functionnal tests using gherkin syntax.

## Use as binary script
Install it:
```bash
$ python3 install -r requirements.txt
$ cp lib/pyppettheater.py /usr/bin/pyppettheater
```

And use it:
```bash
$ /usr/bin/pyppettheater "/path/to/my/yml/file"
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
docker-compose run tests pyppettheater /scenarios/my-suite.yml
docker-compose run tests pyppettheater /scenarios/my-features/my-scenario.feature
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
An actor is a python class which handle sentends. By default the ``Dom`` actor is loaded which can handle these sentences:

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
- The row with ":key" equal to ":value" in table ":table:" should exist
- The row with ":key" equal to ":value" in table ":table:" should not exist
- The row with ":key" equal to ":value" in table ":table:" has ":other_key" equal to ":new_value"
- The row with ":key" equal to ":value" in table ":table:" does not exist
- Then the row with ":key" equal to ":value" in table ":table:" should have ":other_key" equal to ":new_value"

### Rest API
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
 
If you need or want other sentences, open an issue or create a custom actor :)

To load custom actors, you can add a "Actors" section in your yml file, with all relatives paths (relative to the yaml file) to your actors classes:
```yaml
actors:
    - "../actors/custom_actor.py"
```

## Known limitations
- Each feature is session independant: if you are logged in one .feature, you will not be logged in another one
- Because of gherkin comments, you have to escape ``#`` selectors with a ``\``
