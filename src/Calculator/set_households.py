from .models import Household


def set_households(self):
    households = list()
    for idx, row in self.datas.iterrows():
        if "거래 이익" in row.keys():
            household = Household(
                row['name'], row['usage (kWh)'], row['거래 이익']).set_rate(self.contract, self.season)
        else:
            household = Household(
                row['name'], row['usage (kWh)']).set_rate(self.contract, self.season)
        households.append(household)
    self.households = households

    return self
