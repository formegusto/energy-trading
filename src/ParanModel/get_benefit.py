import numpy as np
from ..model import Household


def get_benefit(seller, buyer, log=False, return_price=True):
    if log:
        print(seller.kwh, buyer.kwh)

    if (seller.step_count + 1) == seller.STEP.size:
        return -1

    # 판매 가능 금액
    sell_pos_kwh = seller.STEP[seller.step_count + 1]
    sell_pos_kwh -= seller.kwh

    # buyer simulation, 구매자가 구매했을 때 구매자의 전기요금계 구하기
    buyer_buy_kwh = buyer.kwh - sell_pos_kwh
    # 음수일 경우 구매 불가능.
    if buyer_buy_kwh < 0:
        return -1
    buyer_simulation = Household(
        buyer.name, buyer_buy_kwh).set_rate("단일", "기타")
    before_buyer_price = buyer.basic + buyer.elec_rate
    after_buyer_price = buyer_simulation.basic + buyer_simulation.elec_rate
    # 절감되니까 요금 감소, 전기요금계 상에서 이익으로 동작
    buyer_benefit = before_buyer_price - after_buyer_price
    if log:
        print("구매자 이익 (전기요금계)", buyer_benefit)

    # seller simulation, 판매자가 판매했을 때 판매자의 전기요금계
    seller_sell_kwh = seller.kwh + sell_pos_kwh
    seller_simulation = Household(
        seller.name, seller_sell_kwh).set_rate("단일", "기타")
    before_seller_price = seller.basic + seller.elec_rate
    after_seller_price = seller_simulation.basic + seller_simulation.elec_rate
    # 증가되니까 요금 증가, 전기요금계 상에서 손해로 동작
    seller_loss = after_seller_price - before_seller_price
    if log:
        print("판매자 손해 (전기요금계)", seller_loss)

    # 상품 가치 ((구매자 이익 - 판매자 손해) / 2)
    price_value = np.mean((buyer_benefit + seller_loss) / 2).astype("int")
    if log:
        print("상품가치 {} ~ {}".format(seller_loss, buyer_benefit))
    if log:
        print("추천 거래 가격", price_value)

    # 양쪽 이익
    buyer_benefit -= price_value
    seller_benefit = price_value - seller_loss
    if log:
        print("구매자, 판매자 이익", buyer_benefit, seller_benefit)

    return buyer_benefit
