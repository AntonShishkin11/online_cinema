
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Plan
from app.schemas import PlanCreate, PlanUpdate, PlanOut
import os

router = APIRouter()
INTERNAL_SECRET = os.getenv("INTERNAL_SECRET", "")

def require_internal_secret(x_internal_secret: str = Header(..., alias="X-Internal-Secret")):
    if not INTERNAL_SECRET or x_internal_secret != INTERNAL_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

@router.get("", response_model=list[PlanOut])
async def list_plans(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Plan).order_by(Plan.price))
    return list(res.scalars())

@router.get("/{plan_id}", response_model=PlanOut)
async def get_plan(plan_id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Plan).where(Plan.id == plan_id))
    p = res.scalar_one_or_none()
    if not p:
        raise HTTPException(status_code=404, detail="Plan not found")
    return p

@router.post("", response_model=PlanOut, dependencies=[Depends(require_internal_secret)])
async def create_plan(body: PlanCreate, db: AsyncSession = Depends(get_db)):
    exist = (await db.execute(select(Plan).where(Plan.id == body.id))).scalar_one_or_none()
    if exist:
        raise HTTPException(status_code=409, detail="Plan id already exists")
    p = Plan(**body.dict())
    db.add(p)
    await db.commit()
    await db.refresh(p)
    return p

@router.put("/{plan_id}", response_model=PlanOut, dependencies=[Depends(require_internal_secret)])
async def update_plan(plan_id: str, body: PlanUpdate, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Plan).where(Plan.id == plan_id))
    p = res.scalar_one_or_none()
    if not p:
        raise HTTPException(status_code=404, detail="Plan not found")
    for k, v in body.dict(exclude_unset=True).items():
        setattr(p, k, v)
    await db.commit()
    await db.refresh(p)
    return p

@router.delete("/{plan_id}", dependencies=[Depends(require_internal_secret)])
async def delete_plan(plan_id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Plan).where(Plan.id == plan_id))
    p = res.scalar_one_or_none()
    if not p:
        raise HTTPException(status_code=404, detail="Plan not found")
    await db.delete(p)
    await db.commit()
    return {"ok": True}
