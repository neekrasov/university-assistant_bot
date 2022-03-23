import aiohttp

HOST = 'web'
ai_question_url = "ai-question/"


def create_url(url: str, host: str):
    return f'http://{host}:8000/{url}'


async def simple_post_request(url: str, data: dict = None):
    if data is None:
        data = dict()
    async with aiohttp.ClientSession() as session:
        async with session.post(url=create_url(url, host=HOST), json=data) as response:
            return await response.json()


async def post_ai_request(data: dict):
    return await simple_post_request(url=ai_question_url, data=data)
