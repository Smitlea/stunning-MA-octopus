from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base, Item, Bundle, BundleComponent

engine = create_engine("sqlite:///inventory.db", echo=True)

# 1. 先建表
Base.metadata.create_all(engine)

# 2. 建立初始資料
with Session(engine) as session:
    # 建立所有單品 Item
    items = {
        # 阿熙
        "aixie_badge_a": Item(
            sku="aixie_badge_a",
            name="阿熙 徽章A",
            category="badge",
            stock_qty=100,
        ),
        "aixie_badge_b": Item(
            sku="aixie_badge_b",
            name="阿熙 徽章B",
            category="badge",
            stock_qty=100,
        ),
        "aixie_sticker": Item(
            sku="aixie_sticker",
            name="阿熙 貼紙",
            category="sticker",
            stock_qty=500,
        ),
        "aixie_backcard": Item(
            sku="aixie_backcard",
            name="阿熙 背景紙",
            category="backcard",
            stock_qty=200,
        ),
        "aixie_standee": Item(
            sku="aixie_standee",
            name="阿熙 立牌",
            category="standee",
            stock_qty=50,
        ),

        # 玉米糖
        "corncandy_card": Item(
            sku="corncandy_card",
            name="玉米糖 卡片",
            category="card",
            stock_qty=200,
        ),
        "corncandy_standee": Item(
            sku="corncandy_standee",
            name="玉米糖 立牌",
            category="standee",
            stock_qty=50,
        ),
        "corncandy_sticker": Item(
            sku="corncandy_sticker",
            name="玉米糖 貼紙",
            category="sticker",
            stock_qty=500,
        ),
        "corncandy_backcard": Item(
            sku="corncandy_backcard",
            name="玉米糖 背景紙",
            category="backcard",
            stock_qty=200,
        ),
        "corncandy_badge": Item(
            sku="corncandy_badge",
            name="玉米糖 徽章",
            category="badge",
            stock_qty=100,
        ),

        # 柯樂福
        "clove_badge": Item(
            sku="clove_badge",
            name="柯樂福 徽章",
            category="badge",
            stock_qty=100,
        ),
        "clove_standee": Item(
            sku="clove_standee",
            name="柯樂福 立牌",
            category="standee",
            stock_qty=50,
        ),
        "clove_sticker": Item(
            sku="clove_sticker",
            name="柯樂福 貼紙",
            category="sticker",
            stock_qty=500,
        ),
        "clove_backcard": Item(
            sku="clove_backcard",
            name="柯樂福 背景紙",
            category="backcard",
            stock_qty=200,
        ),

        # 慕 (隱藏款)
        "muo_standee": Item(
            sku="muo_standee",
            name="慕 立牌 (隱藏款)",
            category="standee",
            stock_qty=30,
        ),
    }

    session.add_all(items.values())
    session.flush()  # 先 flush 讓它產生 id，下面可以用

    # 建立四個 bundle
    aixie_bundle = Bundle(
        code="aixie_bundle",
        name="阿熙套組",
        is_hidden=False,
    )
    corncandy_bundle = Bundle(
        code="corncandy_bundle",
        name="玉米糖套組",
        is_hidden=False,
    )
    clove_bundle = Bundle(
        code="clove_bundle",
        name="柯樂福套組",
        is_hidden=False,
    )
    muo_bundle = Bundle(
        code="muo_bundle",
        name="隱藏款 慕",
        is_hidden=True,
    )

    session.add_all([aixie_bundle, corncandy_bundle, clove_bundle, muo_bundle])
    session.flush()

    # 幫每個 bundle 指定需要的零件清單（qty_required 基本都是 1）
    session.add_all(
        [
            # 阿熙套組：兩款徽章+貼紙+背景紙+立牌
            BundleComponent(
                bundle_id=aixie_bundle.id,
                item_id=items["aixie_badge_a"].id,
                qty_required=1,
            ),
            BundleComponent(
                bundle_id=aixie_bundle.id,
                item_id=items["aixie_badge_b"].id,
                qty_required=1,
            ),
            BundleComponent(
                bundle_id=aixie_bundle.id,
                item_id=items["aixie_sticker"].id,
                qty_required=1,
            ),
            BundleComponent(
                bundle_id=aixie_bundle.id,
                item_id=items["aixie_backcard"].id,
                qty_required=1,
            ),
            BundleComponent(
                bundle_id=aixie_bundle.id,
                item_id=items["aixie_standee"].id,
                qty_required=1,
            ),

            # 玉米糖套組：卡片+立牌+貼紙+背景紙+徽章
            BundleComponent(
                bundle_id=corncandy_bundle.id,
                item_id=items["corncandy_card"].id,
                qty_required=1,
            ),
            BundleComponent(
                bundle_id=corncandy_bundle.id,
                item_id=items["corncandy_standee"].id,
                qty_required=1,
            ),
            BundleComponent(
                bundle_id=corncandy_bundle.id,
                item_id=items["corncandy_sticker"].id,
                qty_required=1,
            ),
            BundleComponent(
                bundle_id=corncandy_bundle.id,
                item_id=items["corncandy_backcard"].id,
                qty_required=1,
            ),
            BundleComponent(
                bundle_id=corncandy_bundle.id,
                item_id=items["corncandy_badge"].id,
                qty_required=1,
            ),

            # 柯樂福套組：徽章+立牌+貼紙+背景紙
            BundleComponent(
                bundle_id=clove_bundle.id,
                item_id=items["clove_badge"].id,
                qty_required=1,
            ),
            BundleComponent(
                bundle_id=clove_bundle.id,
                item_id=items["clove_standee"].id,
                qty_required=1,
            ),
            BundleComponent(
                bundle_id=clove_bundle.id,
                item_id=items["clove_sticker"].id,
                qty_required=1,
            ),
            BundleComponent(
                bundle_id=clove_bundle.id,
                item_id=items["clove_backcard"].id,
                qty_required=1,
            ),

            # 慕 (隱藏款)：只有立牌
            BundleComponent(
                bundle_id=muo_bundle.id,
                item_id=items["muo_standee"].id,
                qty_required=1,
            ),
        ]
    )

    session.commit()

    # 範例：算目前「阿熙套組」最多可以賣幾套
    print("阿熙套組可賣(推估):", aixie_bundle.max_bundle_sellable())
    print("玉米糖套組可賣(推估):", corncandy_bundle.max_bundle_sellable())
    print("柯樂福套組可賣(推估):", clove_bundle.max_bundle_sellable())
    print("慕隱藏款可送出(推估):", muo_bundle.max_bundle_sellable())
