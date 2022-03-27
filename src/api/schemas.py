from pydantic import BaseModel


class Question(BaseModel):
    id: int = None
    question: str = None
    answer: str = None

    class Config:
        orm_mode = True


class OnlyQuestionIn(BaseModel):
    question: str = None

    class Config:
        orm_mode = True
