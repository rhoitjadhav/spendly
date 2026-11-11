from langchain_core.tools import tool


class TransactionsTools:
    @tool
    def get_total_spending(self, start_date, end_date) -> int:
        """Get total spending based on start and end period
        e.g. How much did I spend last month?
        Args:
            start_date (str): First period (dd-mm-yyyy).
            end_date (str): Last period (dd-mm-yyyy).

        Returns:
            Total spending for the given period
        """

    @tool
    def get_category_breakdown(
        self, start_date: str, end_date: str, category: str = None
    ):
        """Spend per category, sorted desc. Optional filter to one category.
        e.g. "Where does my money go?" / "How much on Food?" """

    @tool
    def get_summary(self, month=None, year=None):  # "YYYY-MM"
        """Composite month card: total, count, top category, top merchant, avg/day.
        Mirrors your backend MonthSnapshot. e.g. "Overview of October" """

    @tool
    def compare_periods(self, period_a: str, period_b: str):
        """Per-category totals for two periods + deltas computed in SQL.
        e.g. "This month vs last month".
        Args:
            period_a (str): First period (dd-mm-yyyy).
            period_b (str): Second period (dd-mm-yyyy)

        (Composite on purpose: deltas in SQL beat arithmetic by a 9B local model.)"""

    @tool
    def get_top_merchants(self, start_date, end_date, limit=5):
        """Top N merchants by spend. e.g. "Where did most of my money go?" """

    @tool
    def search_transactions(
        self,
        category=None,
        merchant=None,
        date_from=None,
        date_to=None,
        min_amount=None,
        max_amount=None,
        keyword=None,
        limit=20,
    ):
        """List matching transactions, newest first.
        e.g. "Show my Swiggy orders this month" / "my 10 recent transactions" """

    @tool
    def get_spending_average(self, start_date, end_date) -> dict:
        """avg/day, avg/month, tx count. "What's my average spend per day?"
        (mirrors your backend SummaryStats)"""

    @tool
    def get_spending_trend(self, granularity="monthly", periods=6):
        """Totals per month/week as a series. e.g. "Is my spending rising?" """
