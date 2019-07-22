import json
from argparse import ArgumentParser
import utils.config as config


parser = ArgumentParser()
parser.add_argument('--config')
args = parser.parse_args()

if args.config:
    with open(args.config) as file:
        config.config = config.Config.from_dict('config', json.load(file))


from server.server import server
from utils.log import get_logger


log = get_logger('run_server')
log.info('Starting server.')
server.debug = config.config['debug']
server.run()
log.info('Closing up.')
