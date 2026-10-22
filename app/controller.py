from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Note
from app.schema import NoteCreate, NoteUpdate
from fastapi import HTTPException
from sqlalchemy import select

class controller:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def CreateNote(self, note_data: NoteCreate) -> Note:
        new_note = Note(**note_data.dict())
        self.db.add(new_note)
        await self.db.commit()
        await self.db.refresh(new_note)
        return new_note
    
    async def GetNoteById(self, note_id: int) -> Note:
        note = await self.db.get(Note, note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        return note
    
    async def GetNotes(self) -> list[Note]:
        notes = await self.db.execute(select(Note))
        return notes.scalars().all()
    
    async def UpdateNote(self, note_id: int, note_data: NoteUpdate) -> Note:
        note = await self.GetNoteById(note_id)
        note.title = note_data.title
        note.description = note_data.description
        await self.db.commit()
        await self.db.refresh(note)
        return note
    
    async def DeleteNote(self, note_id: int) -> None:
        note = await self.GetNoteById(note_id)
        await self.db.delete(note)
        await self.db.commit()
