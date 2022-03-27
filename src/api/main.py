import uvicorn

from api.schemas import OnlyQuestionIn, Question
from core import ai_assistant
from .app import app


@app.post(path="/ai-question/", response_model=Question)
async def answer_ai(qn: OnlyQuestionIn):
    answer = ai_assistant.ask(qn.question)[0].capitalize()
    return {**qn.dict(), "answer": answer}


@app.get(path="/retraining/")
async def rentaining_ai():
    return {"rentaining_mode": True}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
