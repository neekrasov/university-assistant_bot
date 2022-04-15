import os

import databases
import sqlalchemy
from environs import Env, EnvValidationError

env = Env()
env.read_env()


def get_db_url():
    dp_params = dict()
    for key in ["POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_HOST", "POSTGRES_PORT",
                "POSTGRES_DB"]:
        try:
            value = env.str(key)
        except EnvValidationError:
            value = os.environ[key]
        dp_params[key] = value
    db_url = f"postgresql://{dp_params['POSTGRES_USER']}:{dp_params['POSTGRES_PASSWORD']}@" \
             f"{dp_params['POSTGRES_HOST']}:{dp_params['POSTGRES_PORT']}/{dp_params['POSTGRES_DB']}"
    return db_url


DATABASE_URL = get_db_url()

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
