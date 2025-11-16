import random
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.database import SessionLocal
from app.db.models.requirements import (
    Requirement,
    Contradiction,
    Overlap,
)
from app.db.models.enums import RiskTypeEnum, JurisdictionEnum

# ------------------------------------------
# CONFIGURACIÓN
# ------------------------------------------

NUM_REQUIREMENTS = 300   
NUM_CONTRADICTIONS = 40
NUM_OVERLAPS = 60

# Frases base por categoría
RISK_SENTENCES = {
    RiskTypeEnum.AML: [
        "Firms must implement risk-based AML controls.",
        "Enhanced due diligence is required for high-risk clients.",
        "Suspicious transactions must be monitored continuously.",
    ],
    RiskTypeEnum.FRAUD: [
        "Institutions must maintain strong anti-fraud frameworks.",
        "Transaction anomalies must trigger fraud investigations.",
        "Employees must report indicators of fraudulent behavior.",
    ],
    RiskTypeEnum.CYBERSECURITY: [
        "Systems must include multi-factor authentication.",
        "Data encryption is mandatory for sensitive records.",
        "Organizations must maintain incident response plans.",
    ],
    RiskTypeEnum.GOVERNANCE: [
        "Boards must ensure proper oversight of risk management.",
        "Senior management is accountable for internal controls.",
        "Compliance frameworks must be periodically reviewed.",
    ],
    RiskTypeEnum.PRIVACY: [
        "Personal data must be processed with explicit consent.",
        "Data subjects must be granted access and rectification rights.",
        "Firms must implement storage-limitation policies.",
    ],
    RiskTypeEnum.OPERATIONAL: [
        "Critical operations must have resilience plans.",
        "Firms must document all internal processes.",
        "Incident logs must be recorded and reviewed regularly.",
    ],
    RiskTypeEnum.COMPLIANCE: [
        "Organizations must comply with all relevant legislation.",
        "Internal policies must be aligned with external regulations.",
        "Compliance reports must be filed regularly.",
    ],
    RiskTypeEnum.OTHER: [
        "General provisions must be considered when interpreting rules.",
        "Institutions must remain aware of cross-jurisdiction obligations.",
        "Requirements apply unless explicitly exempted.",
    ],
}

JURISDICTIONS = [
    JurisdictionEnum.EBA,
    JurisdictionEnum.ESMA,
    JurisdictionEnum.ECB,
    JurisdictionEnum.BASEL,
    JurisdictionEnum.FINCEN,
    JurisdictionEnum.FSB,
    JurisdictionEnum.GLOBAL,
    JurisdictionEnum.UK_FCA
]


# ------------------------------------------
# GENERADOR DE REQUISITOS
# ------------------------------------------

def generate_requirement_text(risk: RiskTypeEnum) -> str:
    """Genera texto realista combinando frases base + elementos aleatorios."""
    base = random.choice(RISK_SENTENCES[risk])
    addons = [
        "in accordance with supervisory expectations.",
        "following best international practices.",
        "ensuring proportionality to the institution's size.",
        "subject to periodic review.",
        "with proper documentation retained.",
        "while maintaining adequate governance."
    ]
    return base + " " + random.choice(addons)


# ------------------------------------------
# FUNCIÓN PRINCIPAL
# ------------------------------------------

def seed():
    db: Session = SessionLocal()

    print("🌱 Seeding database with EXTENDED dataset...")

    # Limpieza opcional de tablas
    db.execute(text("DELETE FROM contradictions"))
    db.execute(text("DELETE FROM requirement_overlaps"))
    db.execute(text("DELETE FROM requirements"))
    db.commit()

    all_requirements = []

    # ------------------------------------------
    # 1) Insertar REQUIREMENTS masivos
    # ------------------------------------------
    for i in range(NUM_REQUIREMENTS):
        risk = random.choice(list(RiskTypeEnum))
        req = Requirement(
            text=generate_requirement_text(risk),
            page=random.randint(1, 50),
            line=random.randint(1, 500),
            document_id=None,     # Por ahora None
            risk_type=risk,
            jurisdiction=random.choice(JURISDICTIONS).value
        )
        db.add(req)
        all_requirements.append(req)

        if i > 0 and i % 50 == 0:
            print(f"   Inserted {i} requirements...")

    db.commit()
    db.refresh(all_requirements[0])  # Ensure IDs available

    # ------------------------------------------
    # 2) CONTRADICTIONS
    # ------------------------------------------
    print(f"⚡ Creating {NUM_CONTRADICTIONS} contradictions...")
    for _ in range(NUM_CONTRADICTIONS):
        r1, r2 = random.sample(all_requirements, 2)

        c = Contradiction(
            requirement1_id=r1.id,
            requirement2_id=r2.id,
            description="These requirements conflict based on incompatible obligations.",
            page_1=r1.page,
            line_1=r1.line,
            page_2=r2.page,
            line_2=r2.line,
            jurisdiction=r1.jurisdiction
        )
        db.add(c)

    # ------------------------------------------
    # 3) OVERLAPS
    # ------------------------------------------
    print(f"🌀 Creating {NUM_OVERLAPS} overlaps...")
    for _ in range(NUM_OVERLAPS):
        r1, r2 = random.sample(all_requirements, 2)

        o = Overlap(
            requirement1_id=r1.id,
            requirement2_id=r2.id,
            reason="These requirements overlap due to similar regulatory intent.",
            page_1=r1.page,
            line_1=r1.line,
            page_2=r2.page,
            line_2=r2.line,
            jurisdiction=r1.jurisdiction
        )
        db.add(o)

    db.commit()

    print("🎉 DONE! Database now has:")
    print(f"   → {NUM_REQUIREMENTS} requirements")
    print(f"   → {NUM_CONTRADICTIONS} contradictions")
    print(f"   → {NUM_OVERLAPS} overlaps")


if __name__ == "__main__":
    seed()
