import g4f
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import recommendations, sessions, mood_entries

# Initialize FastAPI app
app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(recommendations.router)
app.include_router(sessions.router)
app.include_router(mood_entries.router)
