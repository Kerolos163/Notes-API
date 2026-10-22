from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.controller import controller
from app.schema import NoteCreate, NoteUpdate

router = APIRouter(prefix="/api", tags=["notes"])

async def get_controller(db: AsyncSession = Depends(get_db)) -> controller:
    return controller(db)

@router.get("/notes")
async def get_notes(
    db: AsyncSession = Depends(get_db),
    ctrl: controller = Depends(get_controller)
    ):
    return await ctrl.GetNotes()

@router.post("/notes")
async def create_note(
    payload: NoteCreate,
    db: AsyncSession = Depends(get_db),
    ctrl: controller = Depends(get_controller),
):
    if payload is None:
        raise HTTPException(status_code=400, detail="Payload is required")
    return await ctrl.CreateNote(payload)

@router.get("/notes/{note_id}")
async def get_note(
    note_id: int, db: AsyncSession = Depends(get_db),
    ctrl: controller = Depends(get_controller)
):
    return await ctrl.GetNoteById(note_id)

@router.put("/notes/{note_id}")
async def update_note(
    note_id: int,
    note_data: NoteUpdate,
    db: AsyncSession = Depends(get_db),
    ctrl: controller = Depends(get_controller)
):
    return await ctrl.UpdateNote(note_id, note_data=note_data) 

@router.delete("/notes/{note_id}")
async def delete_note(
    note_id: int, db: AsyncSession = Depends(get_db),
    ctrl: controller = Depends(get_controller)
):
    return await ctrl.DeleteNote(note_id)
