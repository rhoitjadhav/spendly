class TransactionsTools:
    def get_total_spending(self, start_date, end_date):
        """Total spent + transaction count in a range.
        e.g. "How much did I spend last month?" """

    def get_category_breakdown(self, start_date, end_date, category=None):
        """Spend per category, sorted desc. Optional filter to one category.
        e.g. "Where does my money go?" / "How much on Food?" """

    def get_summary(self, month=None, year=None):  # "YYYY-MM"
        """Composite month card: total, count, top category, top merchant, avg/day.
        Mirrors your backend MonthSnapshot. e.g. "Overview of October" """

    def compare_periods(self, period_a, period_b):
        """Per-category totals for two periods + deltas computed in SQL.
        e.g. "This month vs last month".
        (Composite on purpose: deltas in SQL beat arithmetic by a 9B local model.)"""

    def get_top_merchants(self, start_date, end_date, limit=5):
        """Top N merchants by spend. e.g. "Where did most of my money go?" """

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

    def get_spending_average(self, start_date, end_date) -> dict:
        """avg/day, avg/month, tx count. "What's my average spend per day?"
        (mirrors your backend SummaryStats)"""

    def get_spending_trend(self, granularity="monthly", periods=6):
        """Totals per month/week as a series. e.g. "Is my spending rising?" """
