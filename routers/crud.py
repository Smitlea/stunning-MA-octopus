# app/router/crud.py
from sqlalchemy.orm import Session
from routers import calc
import models, schemas


def create_batch(db: Session, data: schemas.ProductBatchCreate) -> models.ProductBatch:
    """"
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