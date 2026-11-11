from .lendings import LendingsTools
from .run_sql import run_sql
from .transactions import TransactionsTools

transaction_tools = [
    TransactionsTools.get_total_spending,
    TransactionsTools.get_category_breakdown,
    TransactionsTools.get_summary,
    TransactionsTools.compare_periods,
    TransactionsTools.get_top_merchants,
    TransactionsTools.search_transactions,
    TransactionsTools.get_spending_average,
    TransactionsTools.get_spending_trend,
]

lending_tools = [
    LendingsTools.get_lendings,
    LendingsTools.get_lending_summary,
]

default_tools = [run_sql]
