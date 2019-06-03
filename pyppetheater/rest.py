import coloredlogs, json, logging, requests

class Actor():
    def __init__(self, parameters):
        self.base_endpoint = parameters['rest']['base_endpoint']
        self.headers = {}
        self.data = []
        self.request_method = "GET"
        self.logger = logging.getLogger(__name__)
        coloredlogs.install(level='DEBUG', logger=self.logger)

    def set_url(self, url):
        self.url = self.base_endpoint + url

    # I add these headers:
    async def i_add_these_headers(self, headers):
        self.headers = {}
        for header in headers:
            self.headers[header['columns'][0]] = header['columns'][1]

    # I prepare a "GET|POST" request to "url" with data:
    async def i_prepare_a_request_to_with_data(self, request_method, url, request_data):
        self.set_url(url)
        self.request_method = request_method
        self.data = {}
        for data in request_data:
            self.data[data['columns'][0]] = data['columns'][1]

    # I prepare a "GET" request to "url":
    async def i_prepare_a_request_to(self, request_method, url):
        self.set_url(url)
        self.method = request_method
        self.request_method = request_method

    # I send the request
    async def i_send_the_request(self):
        self.last_response = getattr(requests, self.request_method.lower())(self.url, headers=self.headers, data=self.data)

    # Then print the last response
    async def print_the_last_response(self):
        self.logger.info(self.last_response.content)

    # Then print the last json response
    async def print_the_last_json_response(self):
        self.logger.info(self.last_response.json())

    def get_json_node(self, json_data, json_node_name):
        json_node_name = json_node_name.split('.')

        for json_node in json_node_name:
            try:
                json_data = json_data[json_node.replace('[', '').replace(']', '')]
            except:
                json_data = json_data[int(json_node.replace('[', '').replace(']', ''))]
        return json_data

    # And the json node "id" should be equal to "1"
    async def the_json_node_should_be_equal_to(self, json_node_name, json_node_value):
        json_data = self.last_response.json()
        try:
            json_node = self.get_json_node(json_data, json_node_name)
        except:
            await self.print_the_last_json_response()
            raise Exception ('No JSON node "'+json_node_name+' found')

        if str(json_node) != str(json_node_value):
            raise Exception ('The JSON node "'+json_node_name+' is equal to '+str(json_node)+' but '+json_node_value+' expected')

    # The json node "aaaa" should exist
    async def the_json_node_should_exist(self, json_node_name):
        json_data = self.last_response.json()
        try:
            json_node = self.get_json_node(json_data, json_node_name)
        except:
            await self.print_the_last_json_response()
            raise Exception ('No JSON node "'+json_node_name+' found')

    # The json node "aaaa" should not exist
    async def the_json_node_should_not_exist(self, json_node_name):
        json_data = self.last_response.json()
        try:
            json_node = self.get_json_node(json_data, json_node_name)
        except:
            return True
        await self.print_the_last_json_response()
        raise Exception ('JSON node "'+json_node_name+' exist, but it should not')

    # Then the JSON node "" should have "500" elements
    async def the_json_node_should_have_elements(self, json_node_name, nb_elements):
        json_data = self.last_response.json()
        try:
            if json_node_name == "":
                json_node = json_data
            else:
                json_node = self.get_json_node(json_data, json_node_name)
        except:
            await self.print_the_last_json_response()
            raise Exception ('No JSON node "'+json_node_name+' found')

        if len(json_node) != int(nb_elements):
            raise Exception ('The JSON node "'+json_node_name+' contain '+str(len(json_node))+' but '+nb_elements+' was expected')
