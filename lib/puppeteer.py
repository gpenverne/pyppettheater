#!/usr/bin/python3
from test import Test
import asyncio, coloredlogs, logging, os, yaml, sys

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

def test_features(current_path):
    current_dir = os.path.dirname(current_path)
    with open(current_path, 'r') as stream:
        try:
            tests = []
            scenarios = yaml.safe_load(stream)
            for key, scenario in scenarios['scenarios'].items():
                tests.append(Test(os.path.join(current_dir, scenario)))

        except yaml.YAMLError as exc:
            print(exc)
            quit()
    for test in tests:
        asyncio.get_event_loop().run_until_complete(test.start())

current_path = str('/scenarios/' + sys.argv[1]).replace('//', '/')
if not os.path.exists(current_path):
    logger.critical(current_path+' does not exists')
    exit(1)

if ".feature" in current_path:
    asyncio.get_event_loop().run_until_complete(Test(current_path).start())
else:
    test_features(current_path)
