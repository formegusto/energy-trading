from ..model import Household
import numpy as np
import pandas as pd


def simulation_result(self, kwh=None, public_percentage=30):
    if kwh is not None:
        APT = kwh
    elif public_percentage is not None:
        APT = round((self.datas['usage (kWh)'].sum() * 100) /
                    (100 - public_percentage))

    households_count = len(self.datas)
    APT_mean = round(APT / households_count)
    apt_obj = Household("APT", APT_mean).set_rate("단일", "기타")
    apt_price = (apt_obj.basic + apt_obj.elec_rate) * households_count

    before_households_price = np.array(
        [_.basic + _.elec_rate - _.trade_benefit for _ in self.households]).sum()
    self.after_households = np.array([Household(name, kwh, benefit).set_rate("단일", "기타")
                                      for name, kwh, benefit in self.simulation_datas.to_numpy()])
    after_households_price = np.array(
        [_.basic + _.elec_rate - _.trade_benefit for _ in self.after_households]).sum()

    result = pd.DataFrame(columns=['거래 전', '거래 후', '오차'])
    result.loc['세대부 총 가격'] = [before_households_price, after_households_price,
                              after_households_price - before_households_price]

    before_public_price = apt_price - before_households_price
    after_public_price = apt_price - after_households_price
    result.loc['공용부 총 가격'] = [before_public_price,
                              after_public_price, after_public_price - before_public_price]

    result.loc['한 가구 당 공용부 총 가격'] = [before_public_price / households_count,
                                     after_public_price / households_count,
                                     (after_public_price / households_count) - (before_public_price / households_count)]

    return result.astype("int")
