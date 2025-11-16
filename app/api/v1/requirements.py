from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
import random

from app.db.database import get_db
from app.db.models.requirements import Requirement

from app.api.v1.schemas.requirements import (
    RequirementItem,
    RequirementsListResponse,
    SuggestedRequirement,
    SuggestedRequirementsResponse,
    RequirementDetailResponse,
    RequirementNotFound,
)

router = APIRouter(prefix="/requirements", tags=["Requirements"])


# Helper descriptions
SUGGESTED_SENTENCES = [
    "This regulation provides baseline compliance requirements.",
    "A standard obligation that applies across general business operations.",
    "Commonly referenced rule providing essential legal guidance.",
    "General compliance requirement applicable in most jurisdictions.",
    "A typical regulation that ensures baseline regulatory alignment."
]


# ------------------------------------------------------------
# GET /requirements/list  → JSON validated
# ------------------------------------------------------------
@router.get("/list", response_model=RequirementsListResponse)
def list_requirements(
    jurisdiction: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):

    query = db.query(Requirement)

    if jurisdiction:
        query = query.filter(Requirement.jurisdiction == jurisdiction)

    requirements = query.all()

    items = [
        RequirementItem(
            id=req.id,
            text=req.text,
            risk_type=req.risk_type.value if req.risk_type else None,
            jurisdiction=req.jurisdiction,
            page=req.page,
            line=req.line,
            short_description=random.choice(SUGGESTED_SENTENCES)
        )
        for req in requirements
    ]

    return RequirementsListResponse(count=len(items), items=items)


# ------------------------------------------------------------
# GET /requirements/suggested  → JSON validated
# ------------------------------------------------------------
@router.get("/suggested", response_model=SuggestedRequirementsResponse)
def suggested_requirements(
    limit: int = 5,
    jurisdiction: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):

    query = db.query(Requirement)

    if jurisdiction:
        query = query.filter(Requirement.jurisdiction == jurisdiction)

    all_requirements = query.all()

    if not all_requirements:
        return SuggestedRequirementsResponse(count=0, items=[])

    sample = random.sample(all_requirements, min(limit, len(all_requirements)))

    items = [
        SuggestedRequirementItem(
            id=req.id,
            text=req.text,
            risk_type=req.risk_type.value,
            jurisdiction=req.jurisdiction,
            page=req.page,
            line=req.line,
            short_description=random.choice(SUGGESTED_SENTENCES)
        )
        for req in sample
    ]

    return SuggestedRequirementsResponse(count=len(items), items=items)


# ------------------------------------------------------------
# GET /requirements/{id}  → JSON validated
# ------------------------------------------------------------
@router.get("/{requirement_id}", response_model=RequirementDetailResponse | RequirementNotFound)
def get_requirement(requirement_id: int, db: Session = Depends(get_db)):

    req = db.query(Requirement).filter(Requirement.id == requirement_id).first()

    if not req:
        return RequirementNotFound(error="Requirement not found")

    return RequirementDetailResponse(
        id=req.id,
        text=req.text,
        risk_type=req.risk_type.value if req.risk_type else None,
        jurisdiction=req.jurisdiction,
        page=req.page,
        line=req.line,
        description=random.choice(SUGGESTED_SENTENCES)
    )
