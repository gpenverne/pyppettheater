#!/usr/bin/python3
from pyppeteer import launch
from gherkin_parser.parser import parse_from_filename, parse_file, parse_lines
import asyncio, coloredlogs, imp, logging, os, sys, yaml
from .dom import Actor as DomActor
from .mysql import Actor as MysqlActor
from .rest import Actor as RestActor

class Pyppetheater:
    actors = []
    def __init__(self):
        self.page = None
        self.logger = logging.getLogger(__name__)
        coloredlogs.install(level='DEBUG', logger=self.logger)

    def add_actor(self, actor):
        self.actors.append(actor)

    async def start(self, feature_file_name):
        self.feature = parse_from_filename(feature_file_name)
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
                        func_name = func_name.replace(' "'+word.lower()+'"', '')
                        args.append(word)
                        is_opening_quote = False
                    else:
                        is_opening_quote = True

                for actor in self.actors:
                    func_name = func_name.replace(' ', '_').replace(':', '')
                    if not hasattr(actor, func_name):
                        continue
                    try:
                        actor.page = self.page
                        if step['table']:
                            args.append(step['table'])

                        await getattr(actor, func_name)(*args)
                        self.logger.info('\t✅'+stepTitle)
                        break
                    except Exception as e:
                        self.logger.error('\t❌'+stepTitle+'\n')
                        self.logger.critical(str(e)+'\n\n')
                        success = False
                        sys.exit(1)
                        break
                    self.logger.critical('No actor found to play "'+func_name+'"\n\n')
                    sys.exit(1)

            if success:
                self.logger.info('\t (•‿•) '+scenario['title']['content']+'\n\n')
            else:
                await self.take_a_screenshot()
                self.logger.info('\tA screenshot is available for debug (/tmp/screenshot.png)')
                sys.exit(1)

    # Take a screenshot
    async def take_a_screenshot(self):
        await self.page.screenshot({'path': '/tmp/screenshot.png'})

    async def setPage(self):
        if self.page == None:
            self.browser = await launch({"args": ['--no-sandbox']})
            self.page = await self.browser.newPage()

def run_feature_file(theater, feature_file_path):
    return asyncio.get_event_loop().run_until_complete(theater.start(feature_file_path))

def run_yml(yml_path):
    current_dir = os.path.dirname(yml_path)
    theater = Pyppetheater()
    with open(yml_path, 'r') as stream:
        try:
            tests = []
            theater_config = yaml.safe_load(stream)
            try:
                parameters = theater_config['parameters']
            except:
                parameters = []
            theater.add_actor(DomActor(parameters))
            try:
                theater.add_actor(MysqlActor(parameters))
            except:
                pass
            try:
                theater.add_actor(RestActor(parameters))
            except:
                pass
            try:
                actors = theater_config['actors']
            except:
                actors = []
            for actor_path in actors:
                actorTest = imp.load_source(actor_path, os.path.join(current_dir, actor_path))
                theater.add_actor(getattr(actorTest, 'Actor')())
            for key, scenario in theater_config['scenarios'].items():
                run_feature_file(theater, os.path.join(current_dir, scenario))

        except yaml.YAMLError as exc:
            quit()

def run_test(scenario_path):
    if not os.path.exists(scenario_path):
        logger = logging.getLogger(__name__)
        coloredlogs.install(level='DEBUG', logger=logger)
        logger.critical(scenario_path+' does not exists')
        exit(1)

    if ".feature" in scenario_path:
        run_test(scenario_path)
    else:
        run_yml(scenario_path)

if __name__ == "__main__":
    run_test(sys.argv[1])
