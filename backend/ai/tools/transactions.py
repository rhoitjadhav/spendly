from app.db.session import AsyncSessionLocal
from app.models.transaction import Transaction
from app.services.constants import CATEGORIES, Categories
from common.utils import convert_to_date
from langchain_core.tools import tool
from sqlalchemy import func, select


class TransactionsTools:
    @tool
    async def get_total_spending(self, start_date: str, end_date: str) -> int:
        """Get total spending based on start and end period
        e.g. How much did I spend last month?
        Args:
            start_date (str): First period (dd-mm-yyyy).
            end_date (str): Last period (dd-mm-yyyy).

        Returns:
            Total spending for the given period
        """
        start_date = convert_to_date(start_date)
        end_date = convert_to_date(end_date)
        async with AsyncSessionLocal() as session:
            return await session.scalar(
                select(func.coalesce(func.sum(Transaction.amount), 0)).where(
                    Transaction.date.between(start_date, end_date)
                )
            )

    @tool
    async def get_category_breakdown(
        self, start_date: str, end_date: str, category: Categories | None = None
    ):
        """
        Get category breakdown based on start, end period and
        category if mentioned otherwise all categories.

        e.g. Where does my money go?, How much on Food?

        Args:
            start_date (str): First period (dd-mm-yyyy).
            end_date (str): Last period (dd-mm-yyyy).
            category (Categories | None): Categories to filter on.

        """
        stmt = (
            select(
                Transaction.category,
                func.coalesce(func.sum(Transaction.amount), 0).label("total_amount"),
            )
            .group_by(Transaction.category)
            .order_by(Transaction.date.desc())
        )
        if category is None:
            stmt.where(Transaction.date.between(start_date, end_date))
        else:
            stmt.where(
                Transaction.date.between(start_date, end_date),
                Transaction.category == category,
            )
        async with AsyncSessionLocal() as session:
            return session.execute(stmt).all()

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
