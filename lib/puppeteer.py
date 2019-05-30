#!/usr/bin/python3
from pyppettheater import run_test
import asyncio, coloredlogs, logging, os, yaml, sys

scenario_path = str('/scenarios/' + sys.argv[1]).replace('//', '/')
if not os.path.exists(scenario_path):
    logger = logging.getLogger(__name__)
    coloredlogs.install(level='DEBUG', logger=logger)
    logger.critical(scenario_path+' does not exists')
    exit(1)

run_test(scenario_path)
