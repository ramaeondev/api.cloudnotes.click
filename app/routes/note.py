import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import extract, or_
from sqlalchemy.orm import Session, joinedload
from typing import List

import ulid
from app.db.database import get_db
from app.db.models import Category, Note, User
from app.schemas.notes import NoteCreate, NoteResponse, NotesRequest
from app.schemas.response import StandardResponse
from app.schemas.users import UserResponse
from app.security import get_current_user

router = APIRouter(prefix="/v1/notes", tags=["Notes"])
DEFAULT_CATEGORY_NAME = "Uncategorized"

@router.post("/create-note", response_model=StandardResponse, status_code=status.HTTP_201_CREATED)
@router.post("/create-note", response_model=StandardResponse, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not note.date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A date must be provided for the note."
        )

    # Find category by name (if provided)
    category = None
    if note.category_name:
        category = db.query(Category).filter(
            Category.name == note.category_name,
            or_(Category.user_id == user.id, Category.user_id.is_(None))
        ).first()

        # If the category does not exist, create a new one for the user
        if not category:
            category = Category(
                id=ulid.new().str,
                user_id=user.id,
                name=note.category_name,
                color="#FFFFFF"
            )
            db.add(category)
            db.commit()
            db.refresh(category)

    # If no category is found, use "Uncategorized"
    if not category:
        category = db.query(Category).filter(Category.name == DEFAULT_CATEGORY_NAME).first()

    if not category:
        category = Category(
            id=ulid.new().str,
            user_id=None,
            name=DEFAULT_CATEGORY_NAME,
            color="#FFFFFF"
        )
        db.add(category)
        db.commit()
        db.refresh(category)

    category_id = category.id
        # 🔹 **Find the max `order_index` for this date**
    max_order_index = db.query(Note.order_index)\
        .filter(Note.user_id == user.id, Note.date == note.date)\
        .order_by(Note.order_index.desc())\
        .first()

    new_order_index = (max_order_index[0] + 1) if max_order_index else 0

    new_note = Note(
        title=note.title,
        content=note.content,
        user_id=user.id,
        date=note.date,
        category_id=category_id,
        order_index=new_order_index
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return StandardResponse(
        isSuccess=True,
        messages=["Note created successfully"],
        errors=[],
        data=NoteResponse.from_orm(new_note),  # ✅ Use `from_orm()`
        status_code=status.HTTP_201_CREATED
    )

@router.post("/get-all-notes", response_model=StandardResponse)
def get_notes(
    request: NotesRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    notes = (
        db.query(Note)
        .filter(
            Note.user_id == user.id,
            extract('month', Note.date) == request.month,
            extract('year', Note.date) == request.year
        )
        .options(
            joinedload(Note.user),
            joinedload(Note.category), 
            joinedload(Note.attachments)
        )
        .all()
    )

    note_responses = [
        NoteResponse(
            id=note.id,
            title=note.title,
            content=note.content,
            date=note.date,
            pinned=note.pinned,
            order_index=note.order_index,
            is_deleted=note.is_deleted,
            deleted_at=note.deleted_at,
            is_archived=note.is_archived,
            created_at=note.created_at,
            updated_at=note.updated_at,
            user=UserResponse(
                id=note.user.id,
                user_ulid=note.user.user_ulid,
                first_name=note.user.first_name,
                last_name=note.user.last_name,
                email=note.user.email,
                is_active=note.user.is_active, 
            ),
            category=(
                {"id": note.category.id, "name": note.category.name}
                if note.category else None
            ),
            attachments=[
                {"id": att.id, "file_name": att.file_name, "file_url": att.file_url}
                for att in note.attachments
            ]
        )
        for note in notes   
    ]
    return StandardResponse(
        isSuccess=True,
        messages=["Notes retrieved successfully"] if notes else ["No notes found for the selected month and year"],
        data=note_responses,
        status_code=status.HTTP_200_OK
    )
