# app/calc.py
from math import floor
from typing import List, Dict

def run_estimate(
    unit_cost: float,
    hidden_cost: float,
    price: float,
    batch_produced: int,
    expected_sell: int,
):
    """
    販售模式：
    - 商品其實是「一整套系列 = A+B+C」賣 799 元 (price)
    - 每套系列的生產成本 = 3 * unit_cost   (因為 A/B/C 各一個，單個成本90 => 一套270)
    - 每賣出一套系列就會送一個隱藏款，隱藏款成本 hidden_cost (30)

    參數對應：
    - unit_cost:            每一個單品(A或B或C)的成本，例如 90
    - hidden_cost:          隱藏款成本，例如 30
    - price:                一整套系列售價，例如 799
    - batch_produced:       這批你生產了幾套完整系列 (A+B+C都做好的組數)
    - expected_sell:        預估能賣掉幾套完整系列

    回傳:
    - hidden_given:             送出去幾個隱藏款 (等於實際賣掉幾套系列)
    - total_cost:               總成本(壓貨ABC+送出去的隱藏款)
    - total_revenue:            總營收
    - profit:                   淨利
    - margin_percent:           淨利率(%)
    - break_even_sell_count:    至少要賣出幾套系列才不虧
    """

    # 不可能賣超過你做出來的數量
    sold_sets = expected_sell
    if sold_sets > batch_produced:
        sold_sets = batch_produced
    if sold_sets < 0:
        sold_sets = 0

    # 一套系列 = A+B+C
    # ABC 的壓貨成本 (全部先做出來，不管有沒有賣掉)
    base_cost = batch_produced * 3 * unit_cost  # 3 * 90 = 270 一套系列

    # 隱藏款是只有賣掉的那部分才真的送出，所以是變動成本
    hidden_given = sold_sets  # 每賣一套系列就送一個隱藏款
    welfare_cost = hidden_cost * hidden_given   # 30 * 賣出的套數

    # 總成本 = 先壓的ABC + 因為出貨才花到的隱藏款
    total_cost = base_cost + welfare_cost

    # 總營收
    total_revenue = price * sold_sets  # 799 * 實際賣出的套數

    # 淨利
    profit = total_revenue - total_cost

    # 淨利率(%)
    margin_percent = 0.0
    if total_revenue > 0:
        margin_percent = (profit / total_revenue) * 100.0

    # 回本門檻：
    # 對同一批 batch_produced 來說，我至少要賣掉幾套系列才不會虧？
    break_even_sell_count = batch_produced
    for x in range(0, batch_produced + 1):
        # 對「賣掉 x 套系列」來說，營收是多少？
        revenue_x = price * x

        # 成本包含：
        # 1. 這批全部 ABC 壓貨成本 (已經花了，固定 cost)
        # 2. x 份隱藏款成本 (只有賣出去的套才需要送)
        welfare_cost_x = hidden_cost * x
        total_cost_x = base_cost + welfare_cost_x

        profit_x = revenue_x - total_cost_x
        if profit_x >= 0:
            break_even_sell_count = x
            break

    return {
        "hidden_given": hidden_given,
        "total_cost": total_cost,
        "total_revenue": total_revenue,
        "profit": profit,
        "margin_percent": margin_percent,
        "break_even_sell_count": break_even_sell_count,
    }


def run_estimate_series(
    unit_cost: float,              # 單一角色A/B/C的製作成本，例如 90
    hidden_cost: float,            # 隱藏款成本，例如 30
    bundle_price_3: float,         # 三套整組的售價，例如 799
    produced_sets: int,            # 本批打算生產幾「套系列」(一套=ABC各一個)
    buy_rate: float,               # 平均實際售出的比例，例如 0.85 = 85%
):
    """
    假設主要銷售模式是「整套系列 ABC (799) + 送隱藏款」。
    我們用 produced_sets 代表你印了幾套完整系列(ABC都做齊)。
    sold_sets = 實際賣掉幾套系列 (預估 = produced_sets * buy_rate)

    回傳的 dict:
    - hidden_given: 送出去幾個隱藏款 (等於賣掉的整套數)
    - base_cost:    ABC 正常款的壓貨成本總和
    - welfare_cost: 隱藏款贈品的總成本
    - total_cost:   base_cost + welfare_cost
    - revenue:      總營收 (799 * sold_sets)
    - profit:       淨利
    - margin_percent: 淨利率(%)
    - break_even_sell_count: 至少要賣幾套系列才不虧
    """

    # 估計實際賣掉幾套整系列
    sold_sets = round(produced_sets * buy_rate)
    if sold_sets > produced_sets:
        sold_sets = produced_sets  # 不可能賣超過做出來的量

    # 隱藏款數量 = 賣掉幾套整系列
    hidden_given = sold_sets

    # 基礎壓貨成本 (ABC 三款都先做起來)
    # 一套系列 = A(90)+B(90)+C(90)=270
    base_cost = produced_sets * 3 * unit_cost

    # 贈品成本 (只有賣出去的套組才會送隱藏款)
    welfare_cost = hidden_cost * hidden_given

    # 總成本 = 你實際付掉的錢
    total_cost = base_cost + welfare_cost

    # 營收 = 實際賣掉的套數 * 799
    revenue = bundle_price_3 * sold_sets

    # 淨利
    profit = revenue - total_cost

    # 毛利率(淨利 ÷ 營收)
    margin_percent = 0.0
    if revenue > 0:
        margin_percent = (profit / revenue) * 100.0

    # 回本門檻：最少要賣出幾套系列才不虧
    break_even_sell_count = produced_sets
    for x in range(0, produced_sets + 1):
        # 同一批貨的基礎成本是 sunk cost
        base_cost_x = base_cost
        welfare_cost_x = hidden_cost * x
        revenue_x = bundle_price_3 * x
        profit_x = revenue_x - (base_cost_x + welfare_cost_x)
        if profit_x >= 0:
            break_even_sell_count = x
            break

    return {
        "hidden_given": hidden_given,
        "base_cost": base_cost,
        "welfare_cost": welfare_cost,
        "total_cost": total_cost,
        "revenue": revenue,
        "profit": profit,
        "margin_percent": margin_percent,
        "break_even_sell_count": break_even_sell_count,
    }


# def build_forecast_curve_series(
#     unit_cost_per_single: float,   # 90
#     hidden_cost: float,            # 30
#     bundle_price_3: float,         # 799
#     min_produced_sets: int,        # 例如 50
#     max_produced_sets: int,        # 例如 400
#     buy_rate: float,               # 例如 0.85 (85%)
# ) -> List[Dict]:
#     """
#     生成一串資料點，用來畫線圖。
#     x 軸我們用 produced_sets (壓貨多少套系列)
#     y 軸是金額，分別畫：
#       - total_cost     (總成本 = 基礎壓貨成本 + 隱藏款贈品成本)
#       - revenue        (總營收)
#       - welfare_cost   (光是贈品造成的成本)
#       - profit         (淨利)

#     回傳 list[dict]，每個 dict 是一個情境，例如:
#     {
#       "produced_sets": 200,
#       "sold_sets": 170,
#       "base_cost": 54000,
#       "welfare_cost": 5100,
#       "total_cost": 59100,
#       "revenue": 135830,
#       "profit": 76730
#     }
#     """

#     data_points = []

#     for produced_sets in range(min_produced_sets, max_produced_sets + 1):
#         sold_sets = round(produced_sets * buy_rate)
#         if sold_sets > produced_sets:
#             sold_sets = produced_sets

#         # 成本計算 (同上)
#         base_cost = produced_sets * 3 * unit_cost_per_single
#         welfare_cost = hidden_cost * sold_sets
#         total_cost = base_cost + welfare_cost

#         # 收入 & 淨利
#         revenue = bundle_price_3 * sold_sets
#         profit = revenue - total_cost

#         data_points.append({
#             "produced_sets": produced_sets,
#             "sold_sets": sold_sets,
#             "base_cost": base_cost,
#             "welfare_cost": welfare_cost,
#             "total_cost": total_cost,
#             "revenue": revenue,
#             "profit": profit,
#         })

#     return data_points
