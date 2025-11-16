import uuid
from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.database import Base
import enum


# ----------------------
#    ENUM DEFINITIONS
# ----------------------

class CategoryLevel(str, enum.Enum):
    gold = "gold"
    silver = "silver"
    bronze = "bronze"   # Not used now, but kept for future flexibility


class DocumentType(str, enum.Enum):
    eu_leg = "eu_leg"
    financial_regulation = "financial_regulation"
    national_law = "national_law"


# ----------------------
#     DOCUMENT MODEL
# ----------------------

class Document(Base):
    __tablename__ = "documents"

    # Primary key (UUID for clean API design)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Path to the original XML file in /data
    file_path = Column(String, nullable=False)

    # Optional extracted metadata
    title = Column(String, nullable=True)
    jurisdiction = Column(String, nullable=True)

    # Medallion layer classification
    category_level = Column(Enum(CategoryLevel), nullable=False)
    doc_type = Column(Enum(DocumentType), nullable=False)

    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)

    requirements = relationship(
    "Requirement",
    back_populates="document",
    cascade="all, delete-orphan"
)
