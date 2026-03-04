from fastapi import Depends, FastAPI, HTTPException
from typing import List
from uuid import uuid4
from .models import Piece, PieceCreate
from .auth import verify_token

app = FastAPI(title="Pieces Service")

pieces_db: List[Piece] = []

@app.get("/pieces", response_model=List[Piece])
async def get_pieces():
    return pieces_db

@app.post("/pieces", response_model=Piece, status_code=201)
async def create_piece(piece: PieceCreate, auth: str = Depends(verify_token)):
    new_piece = Piece(id=uuid4(), **piece.dict())
    pieces_db.append(new_piece)
    return new_piece

@app.get("/pieces/{piece_id}", response_model=Piece)
async def get_piece(piece_id: str):
    for p in pieces_db:
        if str(p.id) == piece_id:
            return p
    raise HTTPException(status_code=404, detail="Pièce non trouvée")

@app.put("/pieces/{piece_id}", response_model=Piece)
async def update_piece(piece_id: str, piece_update: PieceCreate, auth: str = Depends(verify_token)):
    for i, p in enumerate(pieces_db):
        if str(p.id) == piece_id:
            updated_piece = Piece(id=p.id, **piece_update.dict(), model_id=p.model_id)
            pieces_db[i] = updated_piece
            return updated_piece
    raise HTTPException(status_code=404, detail="Pièce non trouvée")

@app.delete("/pieces/{piece_id}", status_code=204)
async def delete_piece(piece_id: str, auth: str = Depends(verify_token)):
    for i, p in enumerate(pieces_db):
        if str(p.id) == piece_id:
            pieces_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Pièce non trouvée")

@app.get("/pieces/available", response_model=List[Piece])
async def get_available_pieces():
    available = [p for p in pieces_db if p.model_id == 0]
    return available