# app/models.py
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base


class ProductBatch(Base):
    __tablename__ = "product_batches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    # 用來標記這批是什麼，例如 "玉米糖_首發_2025-10"

    unit_cost: Mapped[float] = mapped_column(Float, nullable=False)
    hidden_cost: Mapped[float] = mapped_column(Float, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    batch_produced: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_rule_count: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    scenarios = relationship("ScenarioEstimate", back_populates="batch")


class ScenarioEstimate(Base):
    __tablename__ = "scenario_estimates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    batch_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("product_batches.id", ondelete="CASCADE"), nullable=False
    )

    expected_sell: Mapped[int] = mapped_column(Integer, nullable=False)
    hidden_given: Mapped[int] = mapped_column(Integer, nullable=False)

    total_cost: Mapped[float] = mapped_column(Float, nullable=False)
    total_revenue: Mapped[float] = mapped_column(Float, nullable=False)
    profit: Mapped[float] = mapped_column(Float, nullable=False)
    margin_percent: Mapped[float] = mapped_column(Float, nullable=False)
    break_even_sell_count: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    batch = relationship("ProductBatch", back_populates="scenarios")
