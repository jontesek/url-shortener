from pydantic import BaseModel


class PingResponse(BaseModel):
    status: str

    class Config:
        schema_extra = {"example": {"status": "pong"}}
