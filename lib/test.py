from pyppeteer import launch
from gherkin_parser.parser import parse_from_filename, parse_file, parse_lines
import asyncio, coloredlogs, logging, os, sys, yaml

class Test:
    def __init__(self, feature_file_name):
        self.page = None
        self.logger = logging.getLogger(__name__)
        coloredlogs.install(level='DEBUG', logger=self.logger)
        self.feature = parse_from_filename(feature_file_name)

    async def start(self):
        await self.setPage()
        success = True
        self.logger.info('Feature: ' + self.feature['title']['content'])
        self.logger.info('===========================')
        for scenario in self.feature['scenarios']:
            self.logger.info('\tScenario: ' + scenario['title']['content'])
            self.logger.info('\t---------------------------')
            for step in scenario['steps']:
                stepTitle = step['title']['content'].replace('\#', '#')
                array = stepTitle.split('"')
                func_name = stepTitle.lower()
                args = []
                is_opening_quote = False
                for word in array:
                    if is_opening_quote:
                        func_name = func_name.replace(' "'+word+'"', '')
                        args.append(word)
                        is_opening_quote = False
                    else:
                        is_opening_quote = True
                try:
                    await getattr(self, func_name.replace(' ', '_'))(*args)
                    self.logger.info('\t✅'+stepTitle)
                except Exception as e:
                    self.logger.error('\t❌'+stepTitle+'\n')
                    self.logger.critical(str(e)+'\n\n')
                    success = False
                    break

            if success:
                self.logger.info('\t (•‿•) '+scenario['title']['content']+'\n\n')
            else:
                await self.take_a_screenshot()
                self.logger.info('\tA screenshot is available for debug (screenshot.png)')
                sys.exit(1)

    async def setPage(self):
        if self.page == None:
            self.browser = await launch({"args": ['--no-sandbox']})
            self.page = await self.browser.newPage()

    # I go on "http://myurl"
    async def i_go_on(self, url):
        await self.page.goto(url)

    # Take a screenshot
    async def take_a_screenshot(self):
        await self.page.screenshot({'path': '/scenarios/screenshot.png'})

    # I should be on "http://myurl"
    async def i_should_be_on(self, url):
        pageUrl = self.page.url
        if pageUrl != url:
            raise Exception ('Url is '+pageUrl+' but '+url+' was expected')

    # I type "something" in field "#query"
    async def i_type_in_field(self, value, field_query_selector):
        dom_element = await self.page.querySelector(field_query_selector)
        await self.page.evaluate('(element) => element.value = \'\'', dom_element)
        await self.page.focus(field_query_selector)
        await self.page.keyboard.type(value)

    # I click on "#item"
    async def i_click_on(self, field_query_selector):
        dom_element = await self.page.querySelector(field_query_selector)
        await self.page.evaluate('(btn) => btn.click()', dom_element)
        await self.page.waitForNavigation({})

    # The element "#element" should have "some content" as content
    async def the_element_should_have_as_content(self, field_query_selector, content):
        dom_element = await self.page.querySelector(field_query_selector)
        text = await self.page.evaluate('(element) => element.textContent', dom_element);
        if text != content:
            raise Exception ('Content of '+field_query_selector+' should be "' + str(content) + '", found "'+str(text)+'"')

    # The element "#element" should not exist
    async def the_element_should_not_exist(self, field_query_selector):
        if await self.page.querySelector(field_query_selector) != None:
            raise Exception ('Element "'+field_query_selector+'" has been found in the DOM, but it should not')

    # The element "#element" should exist
    async def the_element_should_exist(self, field_query_selector):
        if await self.page.querySelector(field_query_selector) == None:
            raise Exception ('Element "'+field_query_selector+'" has not been found in the DOM, but it should')
