from typing import Optional
from pydantic import BaseModel
from uuid import UUID, uuid4

class Piece(BaseModel):
    id: UUID
    name: str
    color: str
    quantity: int
    model_id: Optional[int] = 0

class PieceCreate(BaseModel):
    name: str
    color: str
    quantity: int