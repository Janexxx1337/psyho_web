from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict

router = APIRouter()

# Dictionaries to store conversation history and saved sessions
conversation_history: Dict[str, List[Dict]] = {}
saved_sessions: List[Dict] = []

class SessionData(BaseModel):
    session_id: str
    name: str
    age: int
    date: str

@router.post("/save_session")
async def save_session(data: SessionData):
    try:
        # Получаем историю общения из conversation_history
        history = conversation_history.get(data.session_id, [])
        # Сохраняем сессию
        saved_sessions.append({
            "session_id": data.session_id,
            "name": data.name,
            "age": data.age,
            "date": data.date,
            "history": history
        })
        return {"message": "Сессия успешно сохранена"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при сохранении сессии: {str(e)}")

@router.get("/get_sessions")
async def get_sessions():
    return {"sessions": saved_sessions}

@router.get("/get_session_details")
async def get_session_details(session_id: str = Query(..., description="Идентификатор сессии")):
    try:
        # Find the session by session_id
        session = next((s for s in saved_sessions if s['session_id'] == session_id), None)
        if not session:
            raise HTTPException(status_code=404, detail="Сессия не найдена")
        return {"session": session}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении деталей сессии: {str(e)}")
