import g4f
from fastapi import APIRouter, Form, HTTPException
from datetime import datetime
from typing import Dict, List

router = APIRouter()

# Dictionaries to store conversation history
conversation_history: Dict[str, List[Dict]] = {}

@router.post("/get_recommendations")
async def get_recommendations(
        name: str = Form(...),
        age: int = Form(...),
        condition: str = Form(...),
        description: str = Form(...),
        question: str = Form(None),
        session_id: str = Form(...)
):
    try:
        # Initialize conversation history for a new session
        if session_id not in conversation_history:
            conversation_history[session_id] = []

            # Initial prompt to the assistant
            initial_prompt = (
                f"Ты — опытный психолог. Прошу тебя дать рекомендации или поддерживающие слова для человека на основе его ввода. "
                f"Не используй английский язык, не упоминай, что ты ИИ, и не предлагай продолжить задавать вопросы. "
                f"Ответ должен быть полностью на русском языке, без использования английских слов или фраз.\n\n"
                f"Имя клиента: {name} 🌟\n"
                f"Возраст клиента: {age} лет 🎂\n"
                f"Состояние клиента: {condition} 😌\n"
                f"Описание состояния: {description} ✍️\n"
                f"\nПожалуйста, предоставь рекомендации или поддерживающие слова для этого человека, используя только русский язык."
            )
            conversation_history[session_id].append({"role": "user", "content": initial_prompt})

        # Add the user's question if provided
        if question:
            conversation_history[session_id].append({
                "role": "user",
                "content": question,
                "timestamp": datetime.now().strftime("%H:%M")
            })

        # Prepare the messages for the assistant
        messages = conversation_history[session_id]

        # Get the assistant's response
        response = g4f.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=False,  # Changed to False for simplicity
        )

        # Collect the assistant's response
        if isinstance(response, list):
            result = "".join(response)
        else:
            result = response

        # Add the assistant's response to the conversation history
        conversation_history[session_id].append({
            "role": "assistant",
            "content": result,
            "timestamp": datetime.now().strftime("%H:%M")
        })

        return {"recommendations": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при генерации рекомендаций: {str(e)}")
