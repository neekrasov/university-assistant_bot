from environs import Env, EnvValidationError
import os

env = Env()
env.read_env()


def get_bot_token():
    try:
        BOT_TOKEN = env.str("BOT_TOKEN")
    except EnvValidationError:
        BOT_TOKEN = os.environ['BOT_TOKEN']
    return BOT_TOKEN


def get_admins():
    try:
        ADMINS = env.list("ADMINS")
    except EnvValidationError:
        ADMINS = os.environ['ADMINS'].split(',')
    return [int(id) for id in ADMINS]


def get_db_url():
    try:
        DATABASE_URL = env.str("DATABASE_URL")
    except EnvValidationError:
        DATABASE_URL = os.environ['DATABASE_URL']
    return DATABASE_URL


BOT_TOKEN = get_bot_token()
ADMINS = get_admins()
DATABASE_URL = get_db_url()
