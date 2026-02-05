from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db.database import init_db
from app.api.v1 import researchers, auth, users

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Initialize Database Tables on Startup
    init_db()
    yield

app = FastAPI(title="MetalSense API", version="0.1.0", lifespan=lifespan)

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
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to MetalSense API"}