# Pyppettheater

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
docker-compose run tests puppeteer my-scenario.feature
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
Each ``.feature`` is a ghenkins file which contains scenarios about your feature:
```ghenkins
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

## All sentences usable
- I go on "http://myurl"
- Take a screenshot
- I should be on "http://myurl"
- I type "something" in field "#query"
- I click on "#item"
- The element "#element" should have "some content" as content

If you need or want other sentences, open an issue :)

## Known limitations
- Each feature is session independant: if you are logged in one .feature, you will not be logged in another one
- Because of ghenkins comments, you have to escape ``#`` selectores with a ``\``
