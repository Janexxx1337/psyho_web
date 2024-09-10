import g4f
from fastapi import FastAPI, Form, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Инициализация приложения FastAPI
app = FastAPI()

# Настройка CORS (для фронтенда)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Словарь для хранения истории общения по уникальным сессиям
conversation_history = {}
saved_sessions = []  # Список для сохранения сессий

@app.post("/get_recommendations")
async def get_recommendations(
    name: str = Form(...),
    age: int = Form(...),
    condition: str = Form(...),
    description: str = Form(...),
    question: str = Form(None),
    session_id: str = Form(...)
):
    try:
        # Инициализация истории общения для новой сессии
        if session_id not in conversation_history:
            # Сохраняем начальный ввод пользователя в историю
            conversation_history[session_id] = [{
                "role": "user",
                "content": f"Имя клиента: {name}, Возраст клиента: {age} лет, Состояние клиента: {condition}, Описание состояния: {description}"
            }]

            # Добавляем начальный промпт в историю общения
            initial_prompt = (
                f"Ты — опытный психолог. Прошу тебя дать рекомендации или поддерживающие слова для человека на основе его ввода."
                f"Не используй английский язык, не упоминай, что ты ИИ, и не предлагай продолжить задавать вопросы."
                f"Ответ должен быть полностью на русском языке, без использования английских слов или фраз."
                f"\n\nИмя клиента: {name} 🌟\n"
                f"Возраст клиента: {age} лет 🎂\n"
                f"Состояние клиента: {condition} 😌\n"
                f"Описание состояния: {description} ✍️\n"
                f"\nПожалуйста, предоставь рекомендации или поддерживающие слова для этого человека, используя только русский язык."
            )
            conversation_history[session_id].append({"role": "user", "content": initial_prompt})

        # Проверяем, есть ли уточняющий вопрос
        if question:
            # Добавляем уточняющий вопрос в историю
            conversation_history[session_id].append({"role": "user", "content": question})

        # Формируем полный контекст для запроса
        messages = [{"role": "user", "content": conv["content"]} for conv in conversation_history[session_id]]

        # Запрашиваем ответ у модели
        response = g4f.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=True,
        )

        # Собираем ответ от модели
        result = ""
        for message in response:
            result += message

        # Добавляем ответ в историю общения
        conversation_history[session_id].append({"role": "assistant", "content": result})

        return {"recommendations": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при генерации рекомендаций: {str(e)}")

class SessionData(BaseModel):
    session_id: str
    recommendations: str
    name: str
    age: int
    date: str

@app.post("/save_session")
async def save_session(data: SessionData):
    try:
        # Сохранение сессии в список
        saved_sessions.append({
            "session_id": data.session_id,
            "name": data.name,
            "age": data.age,
            "date": data.date,
            "recommendations": data.recommendations,
            "history": conversation_history.get(data.session_id, [])  # Сохраняем историю общения
        })
        return {"message": "Сессия успешно сохранена"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при сохранении сессии: {str(e)}")

@app.get("/get_sessions")
async def get_sessions():
    return {"sessions": saved_sessions}

@app.get("/get_session_details")
async def get_session_details(session_id: str = Query(..., description="Идентификатор сессии")):
    try:
        # Найти сессию по идентификатору
        session = next((s for s in saved_sessions if s['session_id'] == session_id), None)
        if not session:
            raise HTTPException(status_code=404, detail="Сессия не найдена")

        # Добавляем историю общения в сессию
        session["history"] = conversation_history.get(session_id, [])

        # Вернуть детали сессии
        return {"session": session}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении деталей сессии: {str(e)}")
