from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import risks, conflicts, requirements
from app.db.database import Base, engine


# ---------------------------------------------------------
# Initialize DB
# ---------------------------------------------------------
# Important: creates tables if they don’t exist
Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------
# FastAPI App
# ---------------------------------------------------------
app = FastAPI(
    title="REGIS MVP Backend",
    version="1.0.0",
    description="Regulatory Intelligence System (Hackathon MVP)"
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # During hackathon, allow everything
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Routers
# ---------------------------------------------------------
app.include_router(risks.router, prefix="/api/v1/risks", tags=["Risks"])
app.include_router(conflicts.router, prefix="/api/v1/conflicts", tags=["Conflicts"])
app.include_router(requirements.router, prefix="/api/v1/requirements", tags=["Requirements"])


# ---------------------------------------------------------
# Root
# ---------------------------------------------------------
@app.get("/")
def root():
    return {"message": "REGIS Backend running successfully"}
