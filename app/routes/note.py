from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db.models import Note, User
from app.schemas import NoteCreate, NoteResponse
from app.security import get_current_user

router = APIRouter(prefix="/v1/notes", tags=["Notes"])

@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    new_note = Note(**note.dict(), user_id=user_id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@router.get("/", response_model=List[NoteResponse])
def get_notes(db: Session = Depends(get_db), user_id: User = Depends(get_current_user)):
    notes = db.query(Note).filter(Note.user_id == user_id).all()
    return notes