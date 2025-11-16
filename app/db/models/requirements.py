from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.database import Base
from .enums import RiskTypeEnum, JurisdictionEnum
from .document import Document


# =====================================================
# REQUIREMENT
# =====================================================

class Requirement(Base):
    __tablename__ = "requirements"

    id = Column(Integer, primary_key=True, index=True)

    # Texto del requerimiento
    text = Column(Text, nullable=False)

    # Posición dentro del documento
    page = Column(Integer, nullable=True)
    line = Column(Integer, nullable=True)

    # Tipo de riesgo
    risk_type = Column(
        Enum(RiskTypeEnum, name="risk_type_enum"),
        nullable=False,
        index=True
    )

    # Jurisdicción
    jurisdiction = Column(
        String,
        nullable=False,
        index=True,
        default=JurisdictionEnum.GLOBAL.value
    )

    # 🔥 NUEVO - Relación con el documento original
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=True)
    document = relationship("Document")

    # Relaciones con contradicciones y overlaps
    contradictions_as_first = relationship(
        "Contradiction",
        back_populates="requirement1",
        foreign_keys="Contradiction.requirement1_id"
    )

    contradictions_as_second = relationship(
        "Contradiction",
        back_populates="requirement2",
        foreign_keys="Contradiction.requirement2_id"
    )

    overlaps_as_first = relationship(
        "Overlap",
        back_populates="requirement1",
        foreign_keys="Overlap.requirement1_id"
    )

    overlaps_as_second = relationship(
        "Overlap",
        back_populates="requirement2",
        foreign_keys="Overlap.requirement2_id"
    )


# =====================================================
# CONTRADICTIONS
# =====================================================

class Contradiction(Base):
    __tablename__ = "contradictions"

    id = Column(Integer, primary_key=True, index=True)

    requirement1_id = Column(Integer, ForeignKey("requirements.id"), nullable=False)
    requirement2_id = Column(Integer, ForeignKey("requirements.id"), nullable=False)

    # Descripción de por qué se contradicen
    description = Column(Text, nullable=True)

    # Posiciones
    page_1 = Column(Integer, nullable=True)
    line_1 = Column(Integer, nullable=True)
    page_2 = Column(Integer, nullable=True)
    line_2 = Column(Integer, nullable=True)

    jurisdiction = Column(String, nullable=True, index=True)

    requirement1 = relationship(
        "Requirement",
        foreign_keys=[requirement1_id],
        back_populates="contradictions_as_first"
    )

    requirement2 = relationship(
        "Requirement",
        foreign_keys=[requirement2_id],
        back_populates="contradictions_as_second"
    )


# =====================================================
# OVERLAPS
# =====================================================

class Overlap(Base):
    __tablename__ = "requirement_overlaps"

    id = Column(Integer, primary_key=True, index=True)

    requirement1_id = Column(Integer, ForeignKey("requirements.id"), nullable=False)
    requirement2_id = Column(Integer, ForeignKey("requirements.id"), nullable=False)

    # Por qué se solapan
    reason = Column(Text, nullable=True)

    # Posiciones
    page_1 = Column(Integer, nullable=True)
    line_1 = Column(Integer, nullable=True)
    page_2 = Column(Integer, nullable=True)
    line_2 = Column(Integer, nullable=True)

    jurisdiction = Column(String, nullable=True, index=True)

    requirement1 = relationship(
        "Requirement",
        foreign_keys=[requirement1_id],
        back_populates="overlaps_as_first"
    )

    requirement2 = relationship(
        "Requirement",
        foreign_keys=[requirement2_id],
        back_populates="overlaps_as_second"
    )


# =====================================================
# REQUIREMENT EMBEDDINGS
# =====================================================

class RequirementEmbedding(Base):
    __tablename__ = "requirement_embeddings"

    id = Column(Integer, primary_key=True, index=True)

    requirement_id = Column(
        Integer,
        ForeignKey("requirements.id"),
        unique=True,
        nullable=False
    )

    # Embedding como JSON string
    embedding = Column(Text, nullable=False)

    requirement = relationship("Requirement")
