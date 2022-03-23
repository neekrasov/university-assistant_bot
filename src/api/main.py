import uvicorn

from core import ai_assistant
from .app import app
from .db import questions, db
from .schemas import Question, QuestionIn


@app.get(path="/question/{id}", response_model=Question)
async def get_question(pk: int):
    query = questions.select(questions.c.id == pk)
    return {i: g for i, g in (await db.fetch_one(query)).items()}


@app.post(path="/question/", response_model=Question)
async def sreate_questions(qn: QuestionIn):
    query = questions.insert().values(question=qn.question, answer=qn.answer)
    last_record_id = await db.execute(query)
    return {**qn.dict(), "id": last_record_id}


@app.post(path="/ai-question/", response_model=Question)
async def answer_ai(qn: QuestionIn):
    answer = ai_assistant.ask(qn.question)[0].capitalize()
    return {**qn.dict(), "answer": answer}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
