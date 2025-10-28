# app/schemas.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ---------- Batch ----------

class ProductBatchBase(BaseModel):
    name: str = Field(..., description="批次名稱，例如 玉米糖_首發_2025-10")
    unit_cost: float
    hidden_cost: float
    price: float
    batch_produced: int
    bonus_rule_count: int


class ProductBatchCreate(ProductBatchBase):
    pass

class ProductBatchRead(ProductBatchBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True  # pydantic v2用法
    }


# ---------- ScenarioEstimate ----------

class ScenarioCreate(BaseModel):
    expected_sell: int = Field(..., description="假設能賣掉幾套")


class ProductBatchCreate(ProductBatchBase):
    pass


class ScenarioRead(BaseModel):
    id: int
    batch_id: int

    expected_sell: int
    hidden_given: int

    total_cost: float
    total_revenue: float
    profit: float
    margin_percent: float

    break_even_sell_count: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }



# -- Curve---

# class ForecastCurveRequest(BaseModel):
#     min_batch: int = Field(..., description="最少壓貨數量, 例如 50")
#     max_batch: int = Field(..., description="最大壓貨數量, 例如 400")
#     buy_rate: float = Field(0.85, description="預估售出比例, 0.85 = 85%")

# class ForecastCurvePoint(BaseModel):
#     produced: int
#     sold: int
#     welfare_cost: float
#     total_cost: float
#     revenue: float
#     profit: float

# class ForecastCurveResponse(BaseModel):
#     batch_id: int
#     points: list[ForecastCurvePoint]
