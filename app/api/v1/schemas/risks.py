from pydantic import BaseModel
from typing import List, Optional


class RiskItem(BaseModel):
    risk_type: str
    count: int
    percentage: float
    description: str


class RiskSummaryResponse(BaseModel):
    total: int
    risks: List[RiskItem]


class RequirementItem(BaseModel):
    id: int
    text: str
    page: Optional[int]
    line: Optional[int]
    jurisdiction: str


class RiskDetailResponse(BaseModel):
    risk_type: str
    description: str
    count: int
    items: List[RequirementItem]
