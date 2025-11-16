from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, Dict

from app.db.database import get_db
from app.db.models.requirements import Requirement, RiskTypeEnum

from app.api.v1.schemas.risks import (
    RiskDetailResponse,
    RiskSummaryResponse,
    RiskItem,
    RequirementItem
)

router = APIRouter(prefix="/risks", tags=["Risks"])

# ------------------------------------------------------------
# Helper: Simulated descriptions
# ------------------------------------------------------------

RISK_DESCRIPTIONS = {
    RiskTypeEnum.AML: "Anti-Money Laundering risks related to suspicious transactions and weak controls.",
    RiskTypeEnum.FRAUD: "Fraud risk related to misrepresentation or intentional deception.",
    RiskTypeEnum.CYBERSECURITY: "Cybersecurity risks like breaches or unauthorized access.",
    RiskTypeEnum.GOVERNANCE: "Governance risks related to oversight and internal controls.",
    RiskTypeEnum.PRIVACY: "Privacy risks related to GDPR and misuse of personal data.",
    RiskTypeEnum.OPERATIONAL: "Operational risks from process failures or human errors.",
    RiskTypeEnum.COMPLIANCE: "Compliance risks from regulatory violations.",
    RiskTypeEnum.OTHER: "Miscellaneous category for uncategorized risks."
}


# ------------------------------------------------------------
# GET /risks/summary  → JSON validated
# ------------------------------------------------------------
@router.get("/summary", response_model=RiskSummaryResponse)
def risk_summary(
    jurisdiction: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):

    query = db.query(Requirement)

    if jurisdiction:
        query = query.filter(Requirement.jurisdiction == jurisdiction)

    requirements = query.all()

    if not requirements:
        return RiskSummaryResponse(total=0, risks=[])

    total = len(requirements)

    counts: Dict[str, int] = {r.value: 0 for r in RiskTypeEnum}

    for req in requirements:
        counts[req.risk_type.value] += 1

    risks = [
        RiskItem(
            risk_type=risk,
            count=count,
            percentage=round((count / total) * 100, 2),
            description=RISK_DESCRIPTIONS.get(RiskTypeEnum(risk), "No description available.")
        )
        for risk, count in counts.items()
        if count > 0
    ]

    return RiskSummaryResponse(total=total, risks=risks)


# ------------------------------------------------------------
# GET /risks/detail/{risk_type}  → JSON validated
# ------------------------------------------------------------
@router.get("/detail/{risk_type}", response_model=RiskDetailResponse)
def risk_detail(
    risk_type: RiskTypeEnum,
    jurisdiction: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):

    query = db.query(Requirement).filter(Requirement.risk_type == risk_type)

    if jurisdiction:
        query = query.filter(Requirement.jurisdiction == jurisdiction)

    requirements = query.all()

    items = [
        RequirementItem(
            id=req.id,
            text=req.text,
            page=req.page,
            line=req.line,
            jurisdiction=req.jurisdiction
        )
        for req in requirements
    ]

    return RiskDetailResponse(
        risk_type=risk_type.value,
        description=RISK_DESCRIPTIONS.get(risk_type, "No description available."),
        count=len(items),
        items=items
    )
