import math as mt
import numpy as np


def set_cont(self, norm=None):
    if self.energy_trader is None:
        usages = self.meter_month['usage (kWh)'].values
    else:
        _datas = self.energy_trader.datas.copy()
        indexing = self.energy_trader.simulation_datas['usage (kWh)'] > _datas['usage (kWh)']
        new_usage = self.energy_trader.simulation_datas['usage (kWh)'][indexing]
        _datas.loc[indexing, ['usage (kWh)']] = new_usage

        usages = _datas['usage (kWh)'].values
    bins = round(mt.sqrt(usages.size / 2))

    y, x = np.histogram(usages, bins=bins)

    groups = np.zeros(usages.size)
    hist = list()
    for idx, _x in enumerate(x[:-1]):
        start = _x
        end = x[idx + 1]

        hist.append([
            start, end, (start + end) / 2
        ])
        groups[(usages >= start) & (usages <= end)] = idx
    hist = np.array(hist)

    # 재배치
    uni_groups = np.unique(groups).astype("int")
    hist = hist[uni_groups]
    new_groups = np.zeros(usages.size)
    for new_idx, idx in enumerate(uni_groups):
        new_groups[groups == idx] = new_idx
    group_cont = (hist[:, -1] / hist[:, -1].sum())
    self.groups_ = new_groups.astype("int")
    self.cont_ = np.array([group_cont[_] for _ in self.groups_])

    if norm is not None:
        self.cont_ = norm(self.cont_)
