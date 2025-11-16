from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
import random

from app.db.database import get_db
from app.db.models.requirements import Requirement, Contradiction, Overlap

from app.api.v1.schemas.conflicts import (
    RequirementRef,
    ConflictItem,
    ConflictsDetailResponse,
    ConflictsSummaryResponse,
    ConflictSummaryItem
)

router = APIRouter(prefix="/conflicts", tags=["Conflicts"])

# ------------------------------------------------------------
# Fake summaries 
# ------------------------------------------------------------

CONTRADICTION_SENTENCES = [
    "These requirements conflict in scope and compliance interpretation.",
    "The obligations contradict due to incompatible regulatory thresholds.",
    "There is a legal contradiction between applicability conditions.",
    "Operational limits in one rule invalidate obligations in the other.",
    "Interpretation mismatch: requirement A restricts what B mandates.",
]

OVERLAP_SENTENCES = [
    "These requirements cover the same operational scope.",
    "The rules are duplicates with slight wording differences.",
    "Both obligations demand nearly identical compliance actions.",
    "Overlap detected: same policy requirement expressed twice.",
    "Redundant guidance: both regulate the same underlying process.",
]

# ------------------------------------------------------------
# GET /conflicts/summary
# ------------------------------------------------------------
@router.get("/summary", response_model=ConflictsSummaryResponse)
def conflicts_summary(
    jurisdiction: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):

    contradictions_query = db.query(Contradiction)
    overlaps_query = db.query(Overlap)

    if jurisdiction:
        contradictions_query = contradictions_query.filter(Contradiction.jurisdiction == jurisdiction)
        overlaps_query = overlaps_query.filter(Overlap.jurisdiction == jurisdiction)

    contradictions = contradictions_query.count()
    overlaps = overlaps_query.count()

    total = contradictions + overlaps

    if total == 0:
        return ConflictsSummaryResponse(total=0, items=[])

    items = [
        ConflictSummaryItem(
            type="contradiction",
            count=contradictions,
            percentage=round((contradictions / total) * 100, 2),
            description="Cases where two requirements conflict or impose opposing obligations."
        ),
        ConflictSummaryItem(
            type="overlap",
            count=overlaps,
            percentage=round((overlaps / total) * 100, 2),
            description="Cases where two requirements are redundant or partially duplicate."
        )
    ]

    return ConflictsSummaryResponse(total=total, items=items)


# ------------------------------------------------------------
# GET /conflicts/detail/{conflict_type}
# ------------------------------------------------------------
@router.get("/detail/{conflict_type}", response_model=ConflictsDetailResponse)
def conflicts_detail(
    conflict_type: str,
    jurisdiction: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):

    if conflict_type not in ["contradiction", "overlap"]:
        raise ValueError("Invalid conflict type. Use 'contradiction' or 'overlap'.")

    model = Contradiction if conflict_type == "contradiction" else Overlap

    query = db.query(model)

    if jurisdiction:
        query = query.filter(model.jurisdiction == jurisdiction)

    results = query.all()

    items = []
    for item in results:
        r1 = db.query(Requirement).filter(Requirement.id == item.requirement1_id).first()
        r2 = db.query(Requirement).filter(Requirement.id == item.requirement2_id).first()

        items.append(
            ConflictItem(
                id=item.id,
                type=conflict_type,
                jurisdiction=item.jurisdiction,
                description=item.description if conflict_type == "contradiction" else item.reason,
                requirement_1=RequirementRef(
                    id=r1.id,
                    text=r1.text,
                    page=r1.page,
                    line=r1.line,
                    jurisdiction=r1.jurisdiction
                ),
                requirement_2=RequirementRef(
                    id=r2.id,
                    text=r2.text,
                    page=r2.page,
                    line=r2.line,
                    jurisdiction=r2.jurisdiction
                )
            )
        )

    return ConflictsDetailResponse(count=len(items), type=conflict_type, items=items)
