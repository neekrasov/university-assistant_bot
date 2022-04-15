import uvicorn
from typing import List
from .app import app
from .db import questions, db
from .schemas import Question, QuestionIn, QuestionOut


@app.get(path="/question/{id}", response_model=Question)
async def get_question(id: int):
    query = questions.select(questions.c.id == id)
    return {i: g for i, g in (await db.fetch_one(query)).items()}


@app.put(path="/question/", response_model=Question)
async def update_question(qn: QuestionOut):
    query = questions.update().where(questions.c.id == qn.id).values(answer=qn.answer)
    await db.execute(query)
    return {**qn.dict()}


@app.get(path="/question/", response_model=List[Question])
async def get_all_questions():
    query = questions.select()
    return await db.fetch_all(query)


@app.post(path="/question/", response_model=Question)
async def create_question(qn: QuestionIn):
    query = questions.insert().values(question=qn.question)
    last_record_id = await db.execute(query)
    return {**qn.dict(), "id": last_record_id}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
