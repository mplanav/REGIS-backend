from pydantic import BaseModel
from typing import Optional, List


# ---------------------------------------
# Shared structure: Requirement reference
# ---------------------------------------
class RequirementItem(BaseModel):
    id: int
    text: str
    risk_type: Optional[str]
    jurisdiction: str
    page: Optional[int]
    line: Optional[int]
    short_description: Optional[str] = None


# ---------------------------------------
# /requirements/list response
# ---------------------------------------
class RequirementsListResponse(BaseModel):
    count: int
    items: List[RequirementItem]


# ---------------------------------------
# /requirements/suggested response
# ---------------------------------------
class SuggestedRequirement(BaseModel):
    id: int
    text: str
    risk_type: Optional[str]
    jurisdiction: str
    page: Optional[int]
    line: Optional[int]
    short_description: str


class SuggestedRequirementsResponse(BaseModel):
    count: int
    items: List[SuggestedRequirement]


# ---------------------------------------
# /requirements/{id} response
# ---------------------------------------
class RequirementDetailResponse(BaseModel):
    id: int
    text: str
    risk_type: Optional[str]
    jurisdiction: str
    page: Optional[int]
    line: Optional[int]
    description: str


class RequirementNotFound(BaseModel):
    error: str
