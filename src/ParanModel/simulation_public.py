import numpy as np
from ..model import Household


def simulation_public(self, public_percentage=30):
    household_count = len(self.datas)
    APT = round((self.datas['usage (kWh)'].sum() * 100) /
                (100 - public_percentage))
    apt_obj = Household(name="APT", kwh=round(
        APT / household_count)).set_rate("단일", "기타")
    apt_price = (apt_obj.basic + apt_obj.elec_rate) * household_count

    _datas = self.datas.copy()
    before_household_elec_bill = np.array(
        [_.basic + _.elec_rate for _ in self.households]).round().astype("int")
    _datas['전기요금계'] = before_household_elec_bill
    _datas['공용부 요금'] = round(
        (apt_price - before_household_elec_bill.sum()) / household_count)
    _datas['최종청구금액'] = _datas.to_numpy()[:, 2:].sum(axis=1)

    _sim_datas = self.datas.copy()

    after_households = np.array([Household(name, kwh,
                                           self.simulation_datas['거래 이익'].values[idx]
                                           ).set_rate("단일", "기타")
                                 for idx, (name, kwh) in enumerate(self.datas.to_numpy())])
    after_household_elec_bill = np.array([_.basic + _.elec_rate - _.trade_benefit
                                          for _ in after_households]).round().astype("int")
    _sim_datas['전기요금계'] = after_household_elec_bill
    _sim_datas['공용부 요금'] = round(
        (apt_price - after_household_elec_bill.sum()) / household_count)
    _sim_datas['최종청구금액'] = _sim_datas.to_numpy()[:, 2:].sum(axis=1)

    _com_datas = _datas[['name', 'usage (kWh)', '최종청구금액']].copy()
    _com_datas.rename({"최종청구금액": "거래 전 요금"}, inplace=True, axis=1)
    _com_datas['거래 후 요금'] = _sim_datas['최종청구금액']

    _com_datas['오차'] = _com_datas['거래 후 요금'] - _com_datas['거래 전 요금']

    return _datas, _sim_datas, _com_datas
