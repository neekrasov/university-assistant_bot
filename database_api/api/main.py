import uvicorn
from typing import List
from .app import app
from .db import questions, db
from .schemas import Question, QuestionIn


@app.get(path="/question/{id}", response_model=Question)
async def get_question(pk: int):
    query = questions.select(questions.c.id == pk)
    return {i: g for i, g in (await db.fetch_one(query)).items()}


@app.get(path="/question/", response_model=List[Question])
async def get_all_questions():
    query = questions.select()
    # return {i: g for i, g in (await db.fetch_all(query)).items()}
    return await db.fetch_all(query)


@app.post(path="/question/", response_model=Question)
async def create_questions(qn: QuestionIn):
    query = questions.insert().values(question=qn.question, answer=qn.answer)
    last_record_id = await db.execute(query)
    return {**qn.dict(), "id": last_record_id}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
