from ..common import set_init, select_month, set_calc, set_init_csv, inject_trader
from .set_cont import set_cont
from .distribute import distribute, distribute_table
from ...PublicAnalysis.BillTable import BillTable
from .get_result import get_result


class GroupDistributor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.energy_trader = None

    def set_bill_table(self, public_percentage=30):
        self.bill_table = BillTable(
            analyzer=self, public_percentage=public_percentage)


GroupDistributor.set_init = set_init
GroupDistributor.select_month = select_month
GroupDistributor.set_calc = set_calc
GroupDistributor.set_cont = set_cont
GroupDistributor.distribute = distribute
GroupDistributor.distribute_table = distribute_table
GroupDistributor.set_init_csv = set_init_csv
GroupDistributor.inject_trader = inject_trader
GroupDistributor.get_result = get_result
