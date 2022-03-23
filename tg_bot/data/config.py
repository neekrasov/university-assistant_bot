from environs import Env, EnvValidationError
import os

env = Env()
env.read_env()


def get_bot_token():
    try:
        bot_token = env.str("BOT_TOKEN")
    except EnvValidationError:
        bot_token = os.environ['BOT_TOKEN']
    return bot_token


def get_admins():
    try:
        admins = env.list("ADMINS")
    except EnvValidationError:
        admins = os.environ['ADMINS'].split(',')
    return [int(admin_id) for admin_id in admins]


BOT_TOKEN = get_bot_token()
ADMINS = get_admins()
