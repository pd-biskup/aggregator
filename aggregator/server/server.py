from flask import Flask
from utils.config import config
from server.single.server import single_user_server
from server.single.admin import admin_panel
from server.multi.server import multi_user_server
from utils.log import get_logger


log = get_logger('server')
server = Flask(__name__)
if config['mode'] == 'single':
    server.register_blueprint(single_user_server)
    if config['admin']['enabled']:
        server.register_blueprint(admin_panel)
    log.info('Created local single user server.')
elif config['mode'] == 'multi':
    server.register_blueprint(multi_user_server)
    log.info('Created multi user server.')
