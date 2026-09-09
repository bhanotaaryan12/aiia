import os

BASE_DIR = r"c:\Users\nxahw\OneDrive\Desktop\proto\aiia-ctms\backend"

def write_file(path, content):
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# SITE MODEL
write_file("app/models/site.py", """
from sqlalchemy import Column, String, Integer, Date, ForeignKey
from .base import BaseModel

class Site(BaseModel):
    __tablename__ = "sites"
    name = Column(String, nullable=False)
    institution = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    pin_code = Column(String)
    phone = Column(String)
    email = Column(String)
    status = Column(String)
    target_enrollment = Column(Integer)
""")

# PARTICIPANT MODEL
write_file("app/models/participant.py", """
from sqlalchemy import Column, String, Integer, Date, ForeignKey
from .base import BaseModel

class Participant(BaseModel):
    __tablename__ = "participants"
    participant_id = Column(String, unique=True, index=True)
    trial_id = Column(String, ForeignKey("trials.id"))
    site_id = Column(String, ForeignKey("sites.id"))
    screening_date = Column(Date)
    enrollment_date = Column(Date)
    status = Column(String)
    demographics_encrypted = Column(String)
""")

# PHARMACOVIGILANCE MODEL
write_file("app/models/pharmacovigilance.py", """
from sqlalchemy import Column, String, Integer, Date, ForeignKey
from .base import BaseModel

class AdverseEvent(BaseModel):
    __tablename__ = "adverse_events"
    participant_id = Column(String, ForeignKey("participants.id"))
    trial_id = Column(String, ForeignKey("trials.id"))
    site_id = Column(String, ForeignKey("sites.id"))
    event_term = Column(String)
    description = Column(String)
    severity = Column(String)
    seriousness = Column(String)
    causality = Column(String)
    expectedness = Column(String)
    status = Column(String)
""")

# SCHEMAS
write_file("app/schemas/site.py", """
from pydantic import BaseModel
from typing import Optional

class SiteBase(BaseModel):
    name: str
    institution: Optional[str] = None
    city: Optional[str] = None
    status: Optional[str] = None

class SiteCreate(SiteBase):
    pass

class SiteResponse(SiteBase):
    id: str
    class Config:
        from_attributes = True
""")

write_file("app/schemas/participant.py", """
from pydantic import BaseModel
from typing import Optional
from datetime import date

class ParticipantBase(BaseModel):
    participant_id: str
    trial_id: str
    site_id: str
    status: str

class ParticipantCreate(ParticipantBase):
    pass

class ParticipantResponse(ParticipantBase):
    id: str
    class Config:
        from_attributes = True
""")

# ROUTERS
write_file("app/api/v1/sites.py", """
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.core.database import get_db
from app.models.site import Site
from app.schemas.site import SiteResponse, SiteCreate

router = APIRouter()

@router.get("/", response_model=List[SiteResponse])
async def read_sites(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Site).offset(skip).limit(limit))
    return result.scalars().all()

@router.post("/", response_model=SiteResponse)
async def create_site(site_in: SiteCreate, db: AsyncSession = Depends(get_db)):
    new_site = Site(**site_in.model_dump())
    db.add(new_site)
    await db.commit()
    await db.refresh(new_site)
    return new_site
""")

write_file("app/api/v1/participants.py", """
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.core.database import get_db
from app.models.participant import Participant
from app.schemas.participant import ParticipantResponse, ParticipantCreate

router = APIRouter()

@router.get("/", response_model=List[ParticipantResponse])
async def read_participants(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Participant).offset(skip).limit(limit))
    return result.scalars().all()

@router.post("/", response_model=ParticipantResponse)
async def create_participant(participant_in: ParticipantCreate, db: AsyncSession = Depends(get_db)):
    new_participant = Participant(**participant_in.model_dump())
    db.add(new_participant)
    await db.commit()
    await db.refresh(new_participant)
    return new_participant
""")

# UPDATE ROUTER.PY
write_file("app/api/v1/router.py", """
from fastapi import APIRouter
from app.api.v1 import auth, users, trials, sites, participants

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(trials.router, prefix="/trials", tags=["trials"])
api_router.include_router(sites.router, prefix="/sites", tags=["sites"])
api_router.include_router(participants.router, prefix="/participants", tags=["participants"])
""")

# SEED DATA
write_file("app/seed.py", """
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal, engine, Base
from app.models.user import User
from app.models.trial import Trial
from app.core.security import get_password_hash

async def seed_data():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    async with AsyncSessionLocal() as db:
        # Create users
        pwd = get_password_hash("Demo@12345")
        u1 = User(email="admin@aiia.gov.in", username="admin", full_name="Super Admin", hashed_password=pwd, is_superuser=True)
        u2 = User(email="pi@aiia.gov.in", username="pi", full_name="Principal Investigator", hashed_password=pwd)
        db.add_all([u1, u2])
        await db.commit()
        
        # Create trial
        t1 = Trial(title="Ayurveda for Osteoarthritis", short_title="AYU-OA", protocol_number="AYU-2023-01", phase="Phase 3")
        db.add(t1)
        await db.commit()
        
        print("Seed data created successfully.")

if __name__ == "__main__":
    asyncio.run(seed_data())
""")

print("Phase 2 generated successfully.")
