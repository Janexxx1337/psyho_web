# tts.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import torch
import soundfile as sf
from io import BytesIO
from fastapi.responses import StreamingResponse

router = APIRouter()

# Загрузка модели Silero TTS
device = torch.device('cpu')  # Используйте 'cuda' если доступна GPU
model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                     model='silero_tts',
                                     language='ru',
                                     speaker='v3_1_ru')

class TTSRequest(BaseModel):
    text: str

@router.post("/synthesize_speech")
async def synthesize_speech(request: TTSRequest):
    try:
        audio = model.apply_tts(text=request.text,
                                speaker='baya',  # Вы можете выбрать другого спикера
                                sample_rate=8000)
        # Сохранение аудио в байтовый поток
        audio_io = BytesIO()
        sf.write(audio_io, audio, 8000, format='WAV')
        audio_io.seek(0)
        return StreamingResponse(audio_io, media_type='audio/wav')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при синтезе речи: {str(e)}")
