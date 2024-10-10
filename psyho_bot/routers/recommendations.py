import g4f
from fastapi import APIRouter, Form, HTTPException
from typing import Dict, List

router = APIRouter()

# Словарь для хранения истории диалогов
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
        # Инициализация истории диалога для новой сессии
        if session_id not in conversation_history:
            conversation_history[session_id] = []

            # Начальный системный промпт для ассистента
            initial_prompt = (
                f"Ты — опытный психолог-консультант. "
                f"Твоя задача — предоставить профессиональные и эмпатичные рекомендации клиенту на основе его состояния и описания ситуации. "
                f"Отвечай кратко и по делу, избегай лишних слов и повторов. уложись в 900 символов избегая повторо и заканчивая предложения"
                f"Отвечай исключительно на русском языке.\n\n"
                f"Информация о клиенте:\n"
                f"Имя: {name}\n"
                f"Возраст: {age} лет\n"
                f"Состояние: {condition}\n"
                f"Описание проблемы: {description}\n"
            )
            conversation_history[session_id].append({"role": "system", "content": initial_prompt})

        # Добавляем вопрос пользователя, если он предоставлен
        if question:
            conversation_history[session_id].append({
                "role": "user",
                "content": question
            })
            # Добавляем системное сообщение с указанием на краткость
            conversation_history[session_id].append({
                "role": "system",
                "content": "Пожалуйста, отвечай кратко и по делу."
            })

        # Подготовка сообщений для модели (без временных меток и лишних данных)
        messages_for_model = [
            {"role": msg["role"], "content": msg["content"]} for msg in conversation_history[session_id]
        ]

        # Получение ответа от ассистента
        response = g4f.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages_for_model,
            stream=False,
        )

        # Обработка ответа ассистента
        if isinstance(response, list):
            result = "".join(response)
        else:
            result = response

        # Добавляем ответ ассистента в историю диалога
        conversation_history[session_id].append({
            "role": "assistant",
            "content": result
        })

        return {"recommendations": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при генерации рекомендаций: {str(e)}")
