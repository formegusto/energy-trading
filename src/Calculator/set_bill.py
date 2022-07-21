import numpy as np


def set_bill(self):
    # self.apt_won = self.apt_obj.elec_bill_vat_fund * self.household_count
    # self.household_won = np.sum(
    #     [_.elec_bill for _ in self.households])
    # self.public_won = self.apt_won - self.household_won
    self.apt_won = (self.apt_obj.basic +
                    self.apt_obj.elec_rate) * self.household_count
    self.household_won = np.sum(
        [_.basic + _.elec_rate - _.trade_benefit for _ in self.households])
    self.public_won = self.apt_won - self.household_won

    return self
