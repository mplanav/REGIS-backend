import enum

class RiskTypeEnum(str, enum.Enum):
    AML = "AML"
    FRAUD = "FRAUD"
    CYBERSECURITY = "CYBERSECURITY"
    GOVERNANCE = "GOVERNANCE"
    PRIVACY = "PRIVACY"
    OPERATIONAL = "OPERATIONAL"
    COMPLIANCE = "COMPLIANCE"
    OTHER = "OTHER"


class JurisdictionEnum(str, enum.Enum):
    EU = "EU"
    ESMA = "ESMA"
    EBA = "EBA"
    ECB = "ECB"
    BASEL = "Basel"
    FINCEN = "FinCEN"
    FSB = "FSB"
    GLOBAL = "GLOBAL"
    UK_FCA = "UK-FCA"
    OTHER = "OTHER"
