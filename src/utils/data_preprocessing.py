import pandas as pd
import numpy as np
import datetime as dt


def meter_to_metermonth(file_path):
    xlsx = pd.read_excel(file_path, header=None,
                         skiprows=2, engine='openpyxl')

    target_path = "data/meter_month/{}".format(
        file_path.split("/")[-1].split(".")[0])

    print("{} to {}".format(file_path, target_path))

    # 가구명 리스트
    names = xlsx.iloc[:3, 7:]
    names = names.apply(lambda x: "-".join(x.values.astype("str"))).to_numpy()

    # 날짜 리스트
    dates = xlsx.iloc[3:, 1:6]
    dates = dates.apply(lambda x: dt.datetime(
        x[1], x[2], x[3], x[4], x[5]), axis=1).to_numpy()

    usages = xlsx.iloc[3:, 7:].to_numpy()
    usages = np.where(usages == "-", 0, usages)

    # 15분 meter pattern
    meter_15 = pd.DataFrame(
        usages, columns=names, index=dates, dtype=np.float)
    months = np.unique(meter_15.index.month)
    for month in months:
        meter_month = pd.DataFrame(
            np.column_stack([names,
                             meter_15.iloc[meter_15.index.month == month].sum()]),
            columns=['name', 'usage (kWh)']
        )

        meter_month.to_csv("{}_month_{}.csv".format(
            target_path, month), index=False)
