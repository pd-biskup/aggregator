import peewee as sql
from playhouse.postgres_ext import PostgresqlExtDatabase, JSONField
from utils.config import config


db = PostgresqlExtDatabase(config['db']['connection'])
