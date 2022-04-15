from environs import Env

env = Env()
env.read_env()

PERCENTAGE_CONFIDENCE_FOR_ANSWER = env.int('PERCENTAGE_CONFIDENCE_FOR_ANSWER') / 100
