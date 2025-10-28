from __future__ import annotations
from datetime import datetime
from typing import List

from sqlalchemy import (
    String,
    Integer,
    DateTime,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    relationship,
    Mapped,
    mapped_column,
)


class Base(DeclarativeBase):
    pass


# 1. 單一庫存項目：徽章 / 立牌 / 貼紙 / 背景紙 / 卡片 ...
class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # SKU：例如 "aixie_badge_a", "corncandy_card"
    sku: Mapped[str] = mapped_column(String(64), unique=True, index=True)

    # 人類可讀名稱：例如 "阿熙 徽章A", "玉米糖 卡片"
    name: Mapped[str] = mapped_column(String(128), nullable=False)

    # 分類: "badge", "standee", "sticker", "backcard", "card"
    category: Mapped[str] = mapped_column(String(32), nullable=False)

    # 目前庫存數量
    stock_qty: Mapped[int] = mapped_column(Integer, default=0)

    # 安全庫存線（快缺貨提醒用，可自己決定邏輯）
    low_stock_threshold: Mapped[int] = mapped_column(Integer, default=10)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    # 關聯：這個 item 被哪些 bundle 用到
    bundles: Mapped[List["BundleComponent"]] = relationship(
        back_populates="item",
        cascade="all, delete-orphan",
    )


# 2. 套組，例如 "阿熙套組"、"玉米糖套組"、"柯樂福套組"、"隱藏款 慕"
class Bundle(Base):
    __tablename__ = "bundles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # 代號: "aixie_bundle", "corncandy_bundle", "clove_bundle", "muo_bundle"
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True)

    # 展示名稱: "阿熙套組", "玉米糖套組", ...
    name: Mapped[str] = mapped_column(String(128), nullable=False)

    # 是否是隱藏款(限定/贈送) etc.
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    # 關聯: 套組裡有什麼東西
    components: Mapped[List["BundleComponent"]] = relationship(
        back_populates="bundle",
        cascade="all, delete-orphan",
    )

    def max_bundle_sellable(self) -> int:
        """
        推估「我目前最多可以賣出幾套這個 bundle」
        算法 = min( item.stock_qty // component.qty_required ) across all components
        如果這個 bundle 沒設定 components，就回 0
        """
        if not self.components:
            return 0

        possible_counts = []
        for comp in self.components:
            if comp.qty_required <= 0:
                # 理論上不會發生，但避免除以0
                continue
            possible_counts.append(comp.item.stock_qty // comp.qty_required)

        return min(possible_counts) if possible_counts else 0


# 3. 套組↔零件的對照表
#    例如：阿熙套組 需要 阿熙徽章A 1個
class BundleComponent(Base):
    __tablename__ = "bundle_components"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    bundle_id: Mapped[int] = mapped_column(
        ForeignKey("bundles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    item_id: Mapped[int] = mapped_column(
        ForeignKey("items.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # 做一套bundle，需要這個item幾個 (大多數是1)
    qty_required: Mapped[int] = mapped_column(Integer, default=1)

    # 關係
    bundle: Mapped["Bundle"] = relationship(back_populates="components")
    item:   Mapped["Item"]   = relationship(back_populates="bundles")

    # 同一個 bundle 不應該重複同一個 item
    __table_args__ = (
        UniqueConstraint("bundle_id", "item_id", name="uq_bundle_item"),
    )


# 4.（可選）庫存異動紀錄表，方便之後做出貨/補貨log
class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    item_id: Mapped[int] = mapped_column(
        ForeignKey("items.id", ondelete="SET NULL"), nullable=True, index=True
    )

    # 正數 = 入庫(補貨/退貨回倉)，負數 = 出庫(賣掉/報廢)
    delta_qty: Mapped[int] = mapped_column(Integer, nullable=False)

    reason: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        # e.g. "sale_bundle_aixie", "restock_factory", "damaged"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now
    )

    # (方便查紀錄的時候知道是哪個SKU在變動)
    snapshot_sku: Mapped[str] = mapped_column(String(64), nullable=False)
    snapshot_name: Mapped[str] = mapped_column(String(128), nullable=False)
    snapshot_stock_after: Mapped[int] = mapped_column(Integer, nullable=False)
