import json
import utils.config as config


single_user_config = 'single_user_config.json'
with open(single_user_config) as file:
    config.config = config.Config.from_dict('config', json.load(file))


from server.server import server
from utils.log import get_logger


log = get_logger('run_server')
log.info('Starting server.')
server.debug = True
server.run()
log.info('Closing up.')
