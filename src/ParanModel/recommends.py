import numpy as np
from .get_benefit import get_benefit


def recommends(seller, households):
    benefits = np.array([get_benefit(seller, buyer) for buyer in households])

    return np.array([benefits.argmax().astype("int"), benefits.max()])
