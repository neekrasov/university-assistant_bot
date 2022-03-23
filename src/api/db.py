import os

import databases
import sqlalchemy
from environs import Env, EnvValidationError

env = Env()
env.read_env()

try:
    DATABASE_URL = env.str("DATABASE_URL")
except EnvValidationError:
    DATABASE_URL = os.environ['DATABASE_URL']

db = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

questions = sqlalchemy.Table(
    "Question",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("question", sqlalchemy.String),
    sqlalchemy.Column("answer", sqlalchemy.String),
)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)
