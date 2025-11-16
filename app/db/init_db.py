# backend/app/db/init_db.py

from app.db.database import Base, engine

# Import only models that exist and are used
from app.db.models.requirements import (
    Requirement,
    Contradiction,
    Overlap,
    RequirementEmbedding
)

from app.db.models.document import Document

def init_db():
    print(" Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print(" Database ready!")

if __name__ == "__main__":
    init_db()
