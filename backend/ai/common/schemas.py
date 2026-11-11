from pydantic import BaseModel


class ModelQueryRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    chat: str
