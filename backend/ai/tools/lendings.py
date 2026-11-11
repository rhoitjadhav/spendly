from langchain_core.tools import tool


class LendingsTools:
    @tool
    def get_lendings(self, status=None):  # outstanding|repaid
        """From the lendings table: who owes what.
        e.g. "How much does Rahul owe me?" """

    @tool
    def get_lending_summary(self) -> dict:
        """From the lendings table: who owes what."""
