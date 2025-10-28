# app/router/crud.py
from sqlalchemy.orm import Session
from routers import calc
import models, schemas


def create_batch(db: Session, data: schemas.ProductBatchCreate) -> models.ProductBatch:
    """"
    name                           # ID
    unit_cost: float,              # 單一角色A/B/C的製作成本，例如 90
    hidden_cost: float,            # 隱藏款成本，例如 30
    bundle_price_3: float,         # 三套整組的售價，例如 799
    produced_sets: int,            # 本批打算生產幾「套系列」(一套=ABC各一個)
    buy_rate: float,               # 平均實際售出的比例，例如 0.85 = 85%
    """
    batch = models.ProductBatch(
        name=data.name,
        unit_cost=data.unit_cost,
        hidden_cost=data.hidden_cost,
        price=data.price,
        batch_produced=data.batch_produced,
        bonus_rule_count=data.bonus_rule_count,
    )
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch


def get_batch(db: Session, batch_id: int) -> models.ProductBatch | None:
    return db.query(models.ProductBatch).filter(models.ProductBatch.id == batch_id).first()


def list_batches(db: Session):
    return db.query(models.ProductBatch).order_by(models.ProductBatch.created_at.desc()).all()


def create_scenario_for_batch(
    db: Session,
    batch: models.ProductBatch,
    scenario_in: schemas.ScenarioCreate
) -> models.ScenarioEstimate:

    result = calc.run_estimate(
        unit_cost=batch.unit_cost,
        hidden_cost=batch.hidden_cost,
        price=batch.price,
        batch_produced=batch.batch_produced,
        bonus_rule_count=batch.bonus_rule_count,
        expected_sell=scenario_in.expected_sell,
    )

    scenario = models.ScenarioEstimate(
        batch_id=batch.id,
        expected_sell=scenario_in.expected_sell,
        hidden_given=result["hidden_given"],
        total_cost=result["total_cost"],
        total_revenue=result["total_revenue"],
        profit=result["profit"],
        margin_percent=result["margin_percent"],
        break_even_sell_count=result["break_even_sell_count"],
    )

    db.add(scenario)
    db.commit()
    db.refresh(scenario)
    return scenario


def list_scenarios_for_batch(db: Session, batch_id: int):
    return (
        db.query(models.ScenarioEstimate)
        .filter(models.ScenarioEstimate.batch_id == batch_id)
        .order_by(models.ScenarioEstimate.created_at.desc())
        .all()
    )
