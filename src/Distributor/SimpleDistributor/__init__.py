from ..common import set_init, select_month, set_calc
from .distribute import distribute_table, distribute
from .set_cont import set_cont
from ...PublicAnalysis.BillTable import BillTable


class SimpleDistributor:
    def __init__(self, file_path):
        self.file_path = file_path

    def set_bill_table(self, public_percentage=30):
        self.bill_table = BillTable(
            analyzer=self, public_percentage=public_percentage)


SimpleDistributor.set_init = set_init
SimpleDistributor.select_month = select_month
SimpleDistributor.set_calc = set_calc
SimpleDistributor.set_cont = set_cont
SimpleDistributor.distribute = distribute
SimpleDistributor.distribute_table = distribute_table
