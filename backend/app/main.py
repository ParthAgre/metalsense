from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import water_sample
from app.db.database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MetalSense API",
    description="Backend for detecting heavy metal pollution and calculating health risk indices.",
    version="1.0.0"
)

# CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for hackathon/dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(water_sample.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to MetalSense API", "status": "Online"}
