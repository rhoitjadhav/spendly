from enum import StrEnum


class Categories(StrEnum):
    Food = "Food & Dining"
    Transport = "Transport"
    Groceries = "Groceries"
    Shopping = "Shopping"
    Entertainment = "Entertainment"
    Subscriptions = "Subscriptions"
    Health = "Health"
    Recharge = "Recharge"
    Bill = "Bill"
    Rent = "Rent"
    Family = "Family"
    Household = "Household"
    Social = "Social"
    Lending = "Lending"
    Education = "Education"
    Finance = "Finance"
    Uncategorized = "Uncategorized"

    @classmethod
    def values(cls) -> list[str]:
        return [c.value for c in cls]
