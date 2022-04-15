import aiohttp

CORE_HOST = 'core_api'
DB_HOST = 'db_api'
# DB_HOST = '127.0.0.1'
ai_question_url = "ai-question/"
retraining_url = "retraining/"
questions_url = "question/"
question_url = questions_url + '{}'
retraining_urls = "retraining/"
core_api_port = "8002"
db_api_port = "8001"


def create_url(url: str, host: str, port: str, any_id=None):
    if any_id is None:
        any_id = list()
    return f'http://{host}:{port}/{url.format(*any_id)}'


async def simple_post_request(url: str, host: str, port: str, any_id: list = None, data: dict = None):
    if data is None:
        data = dict()
    async with aiohttp.ClientSession() as session:
        async with session.post(url=create_url(url, any_id=any_id, host=host, port=port), json=data) as response:
            return await response.json()


async def simple_get_request(url: str, host: str, port: str, any_id: list = None) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(create_url(url=url, host=host, any_id=any_id, port=port)) as response:
            return await response.json()


async def simple_put_request(url: str, host: str, port: str, any_id: int = None, data: dict = None):
    if data is None:
        data = dict()
    async with aiohttp.ClientSession() as session:
        async with session.put(url=create_url(url, any_id=any_id, host=host, port=port),
                               json=data) as response:
            return await response.json()


async def post_ai_request(data: dict):
    return await simple_post_request(url=ai_question_url, data=data, host=CORE_HOST, port=core_api_port)


async def retraining_get_request():
    return await simple_get_request(url=retraining_url, host=CORE_HOST, port=core_api_port)


async def get_all_questions_request():
    return await simple_get_request(url=questions_url, host=DB_HOST, port=db_api_port)


async def get_question_request(question_id: int):
    return await simple_get_request(url=question_url, host=DB_HOST, any_id=[question_id], port=db_api_port)


async def put_question_request(data: dict):
    return await simple_put_request(url=questions_url, host=DB_HOST, data=data, port=db_api_port)


async def save_question():
    return await simple_get_request(url=questions_url, host=CORE_HOST, port=core_api_port)

#
# if __name__ == "__main__":
#     print(asyncio.run(get_question_request(8)))
