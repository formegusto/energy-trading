import numpy as np
from ..model import Household
from .recommends import recommends
from .after_trade_kwh import after_trade_kwh


def simulation(self):
    simulation_datas = self.datas.copy()
    simulation_datas['거래 가격'] = 0
    simulation_datas['구매 횟수'] = 0
    simulation_datas['판매 횟수'] = 0
    STEP = self.households[0].STEP

    # 시뮬레이션 가구, 누진단계 < 2
    while True:
        sell_pos_households = simulation_datas[simulation_datas['usage (kWh)'] < STEP[1]][[
            'name', 'usage (kWh)']].to_numpy()
        if sell_pos_households.size == 0:
            break
        sell_pos_households = [Household(name, kwh).set_rate(
            "단일", "기타") for name, kwh in sell_pos_households]
        households = [Household(name, kwh).set_rate("단일", "기타")
                      for name, kwh, _ in simulation_datas.iloc[:, :3].to_numpy()]
        reco_values = []
        for seller in sell_pos_households:
            reco_values.append(recommends(seller, households))
        reco_values = np.array(reco_values)

        # 최대 이익 구매자,판매자 파싱
        max_benefit_reco = reco_values[:, 1].argmax()
        max_benefit_seller = sell_pos_households[max_benefit_reco]
        max_benefit_reco = reco_values[max_benefit_reco]
        max_benefit_buyer = households[int(max_benefit_reco[0])]

        # print(max_benefit_seller.kwh, max_benefit_buyer.kwh)
        # print(max_benefit_reco)
        after_seller_kwh, after_buyer_kwh = after_trade_kwh(
            max_benefit_seller, max_benefit_buyer)
        simulation_datas.at[simulation_datas['name'] == max_benefit_seller.name, [
            'usage (kWh)']] = after_seller_kwh
        simulation_datas.at[simulation_datas['name'] ==
                            max_benefit_seller.name, ['거래 가격']] = max_benefit_reco[1]
        simulation_datas.at[simulation_datas['name'] ==
                            max_benefit_seller.name, ['판매 횟수']] = simulation_datas.loc[simulation_datas['name'] ==
                                                                                       max_benefit_seller.name, ['판매 횟수']].values[0] + 1

        simulation_datas.at[simulation_datas['name'] == max_benefit_buyer.name, [
            'usage (kWh)']] = after_buyer_kwh
        before_buyer_trade_price = simulation_datas.loc[simulation_datas['name']
                                                        == max_benefit_buyer.name, ['거래 가격']].values[0]
        simulation_datas.at[simulation_datas['name'] ==
                            max_benefit_buyer.name, ['거래 가격']] = before_buyer_trade_price + max_benefit_reco[1] * -1
        simulation_datas.at[simulation_datas['name'] ==
                            max_benefit_buyer.name, ['구매 횟수']] = simulation_datas.loc[simulation_datas['name'] ==
                                                                                      max_benefit_buyer.name, ['구매 횟수']].values[0] + 1

        self.simulation_datas = simulation_datas
