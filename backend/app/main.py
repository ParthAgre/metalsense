from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import init_db
from app.api.v1.endpoints import researchers # We will create this next

app = FastAPI(title="MetalSense API", version="0.1.0")

# 1. Initialize Database Tables on Startup
@app.on_event("startup")
def on_startup():
    init_db()

# 2. CORS Setup (Essential for your React Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Include Routers
app.include_router(researchers.router, prefix="/api/v1/researcher", tags=["Researcher"])

@app.get("/")
def read_root():
    return {"message": "Welcome to MetalSense API"}