class Actor():
    def __init__(self, parameters):
        pass
    # I go on "http://myurl"
    async def i_go_on(self, url):
        await self.page.goto(url)

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
