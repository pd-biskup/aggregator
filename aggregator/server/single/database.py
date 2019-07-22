from utils.config import config
from utils.log import get_logger


log = get_logger('database')
if config['db']['database'] == 'sqlite':
    import server.single._sqlite
    database = server.single._sqlite.db
    PluginModel = server.single._sqlite.PluginModel
    UserModel = server.single._sqlite.UserModel
elif config['db']['database'] == 'postgres':
    import server.single._postgres
    database = server.single._postgres.db
    PluginModel = server.single._postgres.PluginModel
else:
    log.error(f'Unknown database type: {config["db"]["database"]}')
