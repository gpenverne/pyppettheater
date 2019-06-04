Feature: Use the dom test suite

	Scenario: We can click on links
		Given I go on "https://github.com/gpenverne/pyppettheater"
		Then take a screenshot
		When I click on ".topic-tag.topic-tag-link"
		Then I should be on "https://github.com/topics/puppeteer"
