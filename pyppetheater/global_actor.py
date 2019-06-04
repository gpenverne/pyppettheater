import re
from faker import Faker

class Actor():
    context = {}

    def __init__(self, parameters):
        pass

    def set_context(self, context):
        self.context = {**self.context, **context}

    def parse_value(self, value_to_parse):
        some_value_to_parse = re.sub(r'((.+)?)\<(.+)\>((.+)?)', r'\3', value_to_parse)
        if "context." in some_value_to_parse:
            context_value = self.context[some_value_to_parse.replace('context.', '')]
            value_to_parse = value_to_parse.replace('<'+some_value_to_parse+'>', context_value)
        elif "faker." in some_value_to_parse:
            fake = Faker()
            attribute_name = re.sub(r'((.+)?)\<(.+)\:(.+)\>((.+)?)', r'\3', value_to_parse)
            context_value = getattr(fake, some_value_to_parse.replace('faker.', '').replace(attribute_name+':', ''))()
            value_to_parse = value_to_parse.replace('<'+some_value_to_parse+'>', context_value)
            self.context[attribute_name] = context_value
        value_to_parse = re.sub(r'((.+)?)\<(.+)\>((.+)?)', r'\1\3\4', value_to_parse)
        return value_to_parse
