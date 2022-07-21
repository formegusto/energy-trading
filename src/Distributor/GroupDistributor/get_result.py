import numpy as np
import pandas as pd


def get_result(self):
    dist_df = self.distribute_table()

    before_dist = np.array(
        [_.basic + _.elec_rate - _.trade_benefit for _ in self.calc.households]
    ) + dist_df['공용부요금']
    after_dist = np.array(
        [_.basic + _.elec_rate - _.trade_benefit for _ in self.calc.households]
    ) + dist_df['기여도 요금']

    result = pd.DataFrame()
    result['가구명'] = dist_df['가구명']
    result['가격 분배 전'] = before_dist
    result['가격 분배 후'] = after_dist
    result['오차'] = result['가격 분배 전'] - result['가격 분배 후']

    return result
