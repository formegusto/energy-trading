def after_trade_kwh(seller, buyer):
    # print(seller.kwh, buyer.kwh)
    sell_pos_kwh = seller.STEP[seller.step_count + 1]
    sell_pos_kwh -= seller.kwh

    seller_sell_kwh = seller.kwh + sell_pos_kwh
    buyer_buy_kwh = buyer.kwh - sell_pos_kwh

    return seller_sell_kwh, buyer_buy_kwh
