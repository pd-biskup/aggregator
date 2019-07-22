import peewee as sql
from playhouse.sqlite_ext import SqliteExtDatabase, JSONField
from utils.config import config
from utils.log import get_logger


def connect() -> SqliteExtDatabase:
    log = get_logger('sqlite')
    log.debug(f'Connecting to {config["db"]["connection"]} sqlite database.')
    return SqliteExtDatabase(config['db']['connection'])


db = connect()


class UserModel(sql.Model):

    id = sql.PrimaryKeyField()
    username = sql.CharField(null=False, unique=True)
    password = sql.CharField(null=True, default=None)
    settings = JSONField(null=True, default=None)

    class Meta:
        database = db


class PluginModel(sql.Model):

    id = sql.PrimaryKeyField()
    user = sql.ForeignKeyField(UserModel, 'id', 'plugins')
    plugin = sql.TextField(null=False)
    params = JSONField(null=False, default={})
    data = JSONField(null=False, default={})

    class Meta:
        database = db


db.create_tables([UserModel, PluginModel])
db.close()
