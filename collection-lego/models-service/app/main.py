from fastapi import FastAPI, HTTPException
from typing import List
from uuid import UUID, uuid4
from pydantic import BaseModel
import httpx

PIECES_SERVICE_URL = "http://127.0.0.1:8000"
SECRET_TOKEN = "TOKEN_SECRET"

app = FastAPI(title="Models Service")

models_db = []

class Model(BaseModel):
    id: UUID
    name: str
    pieces: List[UUID] = []

class ModelCreate(BaseModel):
    name: str


@app.get("/models", response_model=List[Model])
async def get_models():
    return models_db

@app.post("/models", response_model=Model, status_code=201)
async def create_model(model: ModelCreate):
    new_model = Model(id=uuid4(), name=model.name)
    models_db.append(new_model)
    return new_model

@app.post("/models/{model_id}/pieces/{piece_id}", response_model=Model)
async def add_piece_to_model(model_id: str, piece_id: str):
    model = next((m for m in models_db if str(m.id) == model_id), None)
    if not model:
        raise HTTPException(status_code=404, detail="Modèle non trouvé")
    
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{PIECES_SERVICE_URL}/pieces/{piece_id}",
            headers={"Authorization": f"Bearer {SECRET_TOKEN}"},
            json={"name": "ignored", "color": "ignored", "quantity": 1}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Update de la pièce échoué")

    if UUID(piece_id) not in model.pieces:
        model.pieces.append(UUID(piece_id))

    return model