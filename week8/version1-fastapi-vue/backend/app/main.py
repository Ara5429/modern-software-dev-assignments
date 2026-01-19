from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import notes, moods, tags, action_items
from app.database import init_db

app = FastAPI(
    title="Mood Tracker API",
    description="A note-taking app with mood tracking",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()
    print("🚀 Server started successfully!")

# Include routers
app.include_router(notes.router)
app.include_router(moods.router)
app.include_router(tags.router)
app.include_router(action_items.router)

@app.get("/")
def read_root():
    return {
        "message": "Mood Tracker API",
        "docs": "/docs",
        "version": "1.0.0"
    }
