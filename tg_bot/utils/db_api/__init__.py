import aiohttp

HOST = 'core_api'
ai_question_url = "ai-question/"
retraining_url = "retraining/"
core_api_port = "8000"
database_api_port = "8001"


def create_url(url: str, host: str, any_id=None):
    if any_id is None:
        any_id = list()
    return f'http://{host}:8000/{url.format(*any_id)}'


async def simple_post_request(url: str, any_id: list = None, data: dict = None):
    if data is None:
        data = dict()
    async with aiohttp.ClientSession() as session:
        async with session.post(url=create_url(url, any_id=any_id, host=HOST), json=data) as response:
            return await response.json()


async def simple_get_request(url: str, any_id: list = None) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(create_url(url=url, host=HOST, any_id=any_id)) as response:
            return await response.json()


async def post_ai_request(data: dict):
    return await simple_post_request(url=ai_question_url, data=data)


async def retraining_get_request():
    return await simple_get_request(url=retraining_url)
