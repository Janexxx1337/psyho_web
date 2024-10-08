from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, List

router = APIRouter()

mood_entries_db: Dict[str, List[Dict]] = {}

# Модель для записи настроения
class MoodEntry(BaseModel):
    user_id: str
    date: str
    rating: int
    comment: str

@router.post("/save_mood_entry")
async def save_mood_entry(entry: MoodEntry):
    try:
        user_id = entry.user_id
        if user_id not in mood_entries_db:
            mood_entries_db[user_id] = []
        mood_entries_db[user_id].append({
            "date": entry.date,
            "rating": entry.rating,
            "comment": entry.comment
        })
        return {"message": "Запись настроения сохранена."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при сохранении записи настроения: {str(e)}")

@router.get("/get_mood_entries")
async def get_mood_entries(user_id: str = Query(..., description="Идентификатор пользователя")):
    try:
        entries = mood_entries_db.get(user_id, [])
        return {"entries": entries}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении записей настроения: {str(e)}")

@router.get("/get_mood_analysis")
async def get_mood_analysis(user_id: str = Query(..., description="Идентификатор пользователя")):
    try:
        entries = mood_entries_db.get(user_id, [])
        if not entries:
            return {"analysis": "Нет данных для анализа."}

        average_rating = sum(entry['rating'] for entry in entries) / len(entries)
        if average_rating < 5:
            analysis = "Ваше среднее настроение низкое. Рекомендуем обратить внимание на ваше эмоциональное состояние."
        else:
            analysis = "Ваше настроение в норме. Продолжайте в том же духе!"

        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при анализе настроений: {str(e)}")
