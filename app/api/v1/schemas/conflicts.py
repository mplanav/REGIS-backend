from pydantic import BaseModel
from typing import List, Optional


class RequirementRef(BaseModel):
    id: int
    text: str
    page: Optional[int]
    line: Optional[int]
    jurisdiction: str


class ConflictItem(BaseModel):
    id: int
    type: str
    jurisdiction: Optional[str]
    description: Optional[str]
    requirement_1: RequirementRef
    requirement_2: RequirementRef


class ConflictSummaryItem(BaseModel):
    type: str
    count: int
    percentage: float
    description: str


class ConflictsSummaryResponse(BaseModel):
    total: int
    items: List[ConflictSummaryItem]


class ConflictsDetailResponse(BaseModel):
    count: int
    type: str
    items: List[ConflictItem]
