import uvicorn

from api.schemas import QuestionIn, Question
from core import ai_assistant
from .app import app

from loguru import logger


@app.post(path="/ai-question/", response_model=Question)
async def answer_ai(qn: QuestionIn):
    logger.debug(qn.question)
    answer = ai_assistant.ask(qn.question)
    logger.debug(answer)
    return {**qn.dict(), "answer": answer}


@app.get(path="/retraining/")
async def rentaining_ai():
    return {"rentaining_mode": True}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
