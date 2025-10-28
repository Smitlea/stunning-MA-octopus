# app/routers/batches.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from routers import crud, calc
import models, schemas
from database import get_db, Base, engine

# 確保第一次啟動時建表
Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post("/", response_model=schemas.ProductBatchRead)
def create_product_batch(
    batch_in: schemas.ProductBatchCreate,
    db: Session = Depends(get_db),
):
    batch = crud.create_batch(db, batch_in)
    return batch


@router.get("/", response_model=List[schemas.ProductBatchRead])
def list_product_batches(db: Session = Depends(get_db)):
    return crud.list_batches(db)


@router.get("/{batch_id}", response_model=schemas.ProductBatchRead)
def get_product_batch(batch_id: int, db: Session = Depends(get_db)):
    batch = crud.get_batch(db, batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    return batch

@router.post("/{batch_id}/scenario", response_model=schemas.ScenarioRead)
def create_scenario(
    batch_id: int,
    scenario_in: schemas.ScenarioCreate,
    db: Session = Depends(get_db),
):
    batch = crud.get_batch(db, batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    scenario = crud.create_scenario_for_batch(db, batch, scenario_in)
    return scenario


@router.get("/{batch_id}/scenarios", response_model=List[schemas.ScenarioRead])
def list_scenarios(batch_id: int, db: Session = Depends(get_db)):
    batch = crud.get_batch(db, batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    return crud.list_scenarios_for_batch(db, batch_id)


# @router.post("/{batch_id}/forecast_curve", response_model=schemas.ForecastCurveResponse)
# def forecast_curve(
#     batch_id: int,
#     req: schemas.ForecastCurveRequest,
#     db: Session = Depends(get_db),
# ):
#     batch = crud.get_batch(db, batch_id)
#     if not batch:
#         raise HTTPException(status_code=404, detail="Batch not found")

#     points = calc.build_forecast_curve_series(
#         unit_cost=batch.unit_cost,
#         hidden_cost=batch.hidden_cost,
#         price=batch.price,
#         bonus_rule_count=batch.bonus_rule_count,
#         min_batch=req.min_batch,
#         max_batch=req.max_batch,
#         buy_rate=req.buy_rate,
#     )

#     return {
#         "batch_id": batch.id,
#         "points": points,
#     }
