import datetime
import logging
from fastapi import APIRouter, Depends, HTTPException, Query, logger, status
from sqlalchemy import extract, func, or_
from sqlalchemy.orm import Session, joinedload
from typing import Optional
from datetime import datetime

import ulid
from app.db.database import get_db
from app.db.models import Category, Note, User
from app.schemas.notes import CategoryResponse, NoteCreate, NoteResponse, NotesRequest
from app.schemas.response import StandardResponse
from app.schemas.users import UserResponse
from app.security import get_current_user

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter(prefix="/v1/notes", tags=["Notes"])
DEFAULT_CATEGORY_NAME = "Uncategorized"

# Not using in the UI now Moved to create-or-update-note
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

# Not using in the UI now moved to get-all-notes get
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

@router.post("/create-or-update-note", response_model=StandardResponse, status_code=status.HTTP_201_CREATED)
def create_or_update_note(
    note: NoteCreate, 
    db: Session = Depends(get_db), 
    user: User = Depends(get_current_user)
):
    existing_note = None
    if note.note_id:
        existing_note = db.query(Note).filter(
            Note.id == note.note_id, Note.user_id == user.id
        ).first()

    if existing_note:
        # 🔹 **Update only title & content, ignore date**
        existing_note.title = note.title
        existing_note.content = note.content

        db.commit()
        db.refresh(existing_note)

        return StandardResponse(
            isSuccess=True,
            messages=["Note updated successfully"],
            errors=[],
            data=NoteResponse.from_orm(existing_note),
            status_code=status.HTTP_200_OK
        )

    # 🔹 **For new notes, `date` is required**
    if not note.date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A date must be provided for new notes."
        )

    # 🔹 **Find category by name (if provided)**
    category = None
    if note.category_name:
        category = db.query(Category).filter(
            Category.name == note.category_name,
            or_(Category.user_id == user.id, Category.user_id.is_(None))
        ).first()

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

    # 🔹 **Find max `order_index` for this date**
    max_order_index = db.query(Note.order_index)\
        .filter(Note.user_id == user.id, Note.date == note.date)\
        .order_by(Note.order_index.desc())\
        .first()

    new_order_index = (max_order_index[0] + 1) if max_order_index else 0

    # 🔹 **Create a new note**
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
        data=NoteResponse.from_orm(new_note),
        status_code=status.HTTP_201_CREATED
    )

@router.get("/get-all-notes", response_model=StandardResponse)
def get_notes(
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    try:
        logger.info(f"Received request for note count on date: {date}")
        selected_date = datetime.strptime(date, "%Y-%m-%d").date()
        logger.info(f"Parsed selected date: {selected_date}")

        # Extract month and year for debugging
        month, year = selected_date.month, selected_date.year
        logger.info(f"Extracted Month: {month}, Year: {year}")

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    notes = (
        db.query(Note)
        .filter(
            Note.user_id == user.id,
            func.date(Note.date) == selected_date  # This ensures it ignores time
        )
        .options(
            joinedload(Note.user),
            joinedload(Note.category),
            joinedload(Note.attachments)
        )
        .all()
    )
    
    logger.info(f"📝 Fetched {len(notes)} notes for date: {selected_date}")

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
                {"id": note.category.id, 
                "numeric_id": note.category.numeric_id,
                "color": note.category.color,
                 "name": note.category.name
                 }
                if note.category else None
            ),
            attachments=[
                {"id": att.id, "file_name": att.file_name, "file_url": att.file_url}
                for att in note.attachments
            ]
        )
        for note in notes   
    ]
    
    logger.info(f"✅ Returning {len(note_responses)} notes in response.")
    return StandardResponse(
        isSuccess=True,
        messages=["Notes retrieved successfully"] if notes else ["No notes found for the selected date"],
        data=note_responses,
        status_code=status.HTTP_200_OK
    )
 
@router.post("/get-all-notes-count", response_model=StandardResponse)
def get_notes_count(
    request: NotesRequest,  # Expecting month and year in request body
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # Fetch note counts grouped by date and category
    notes_count = (
        db.query(Note.date, Note.category_id, func.count(Note.id).label("count"))
        .filter(
            Note.user_id == user.id,
            extract('month', Note.date) == request.month,
            extract('year', Note.date) == request.year
        )
        .group_by(Note.date, Note.category_id)
        .all()
    )

    # Transform data into a structured format
    counts_by_date = {}
    for note_date, category_id, count in notes_count:
        date_str = note_date.strftime("%Y-%m-%d")  # Convert date to string
        if date_str not in counts_by_date:
            counts_by_date[date_str] = []
        counts_by_date[date_str].append({"category_id": category_id, "count": count})
        category = db.query(Category).filter(Category.id == category_id).first()
        counts_by_date[date_str].append({
            "category_id": category_id,
            "numeric_id": category.numeric_id if category else None,
            "name": category.name if category else DEFAULT_CATEGORY_NAME,
            "color": category.color if category else "#FFFFFF",
            "count": count
        })

    return StandardResponse(
        isSuccess=True,
        messages=["Note counts retrieved successfully"],
        data=counts_by_date,
        status_code=status.HTTP_200_OK
    )

@router.get("/categories", response_model=StandardResponse)
def get_categories(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    categories = db.query(Category).filter(Category.user_id == user.id).all()
    
    category_responses = [
        CategoryResponse(
            id=cat.id,
            numeric_id=cat.numeric_id,
            name=cat.name,
            color=cat.color
        )
        for cat in categories
    ]

    return StandardResponse(
        isSuccess=True,
        messages=["Categories retrieved successfully"],
        data=category_responses,
        status_code=status.HTTP_200_OK
    )
