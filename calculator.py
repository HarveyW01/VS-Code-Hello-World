from datetime import date, datetime
from typing import Tuple

# Fine rates per day by item category
RATES: dict[str, float] = {
    "Standard": 0.50,
    "Best-Seller": 1.00,
    "DVD": 2.00,
}

# Discount rates by membership tier
DISCOUNTS: dict[str, float] = {
    "Senior": 0.50,
    "Student": 0.20,
    "Adult": 0.00,
}

MAX_FINE: float = 15.00


def get_member_type() -> str:
    """Prompt user for member selection and return the member type."""
    choice = input("Member (1: Adult, 2: Student, 3: Senior): ").strip()
    return {"1": "Adult", "2": "Student", "3": "Senior"}.get(choice, "Adult")


def get_item_type() -> str:
    """Prompt user for item selection and return the item type."""
    choice = input("Enter 1 for Standard, 2 for Best-Seller, 3 for DVD: ").strip()
    return {"1": "Standard", "2": "Best-Seller", "3": "DVD"}.get(choice, "Standard")


def calculate_days_late(due_date: date, return_date: date) -> int:
    """Calculate and return the non-negative number of days late."""
    return max(0, (return_date - due_date).days)


def calculate_fine(
    days_late: int, item_type: str, member_type: str
) -> Tuple[float, float, float]:
    """Calculate base fine, discount, and final capped fine rounded to two decimal places."""
    daily_rate = RATES.get(item_type, 0.50)
    discount_rate = DISCOUNTS.get(member_type, 0.00)

    base_fine = round(days_late * daily_rate, 2)
    discount_amount = round(base_fine * discount_rate, 2)
    fine_after_discount = round(base_fine - discount_amount, 2)
    final_fine = min(MAX_FINE, fine_after_discount)

    return base_fine, discount_amount, final_fine


def print_fine_summary(
    days_late: int, base_fine: float, discount_amount: float, final_fine: float
) -> None:
    """Display formatted fine calculation results."""
    print(f"\nDays Late: {days_late}")
    print(f"Base Fine: ${base_fine:.2f}")
    print(f"Discount Applied: ${discount_amount:.2f}")
    print(f"Final Fine: ${final_fine:.2f}")


def parse_date(prompt: str) -> date:
    """Prompt for and parse a date string in YYYY-MM-DD format."""
    date_str = input(prompt).strip()
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def main() -> None:
    member_type = get_member_type()
    item_type = get_item_type()

    try:
        due_date = parse_date("Enter due date (YYYY-MM-DD): ")
        return_date = parse_date("Enter return date (YYYY-MM-DD): ")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        raise SystemExit(1)

    days_late = calculate_days_late(due_date, return_date)
    base_fine, discount_amount, final_fine = calculate_fine(
        days_late, item_type, member_type
    )

    print_fine_summary(days_late, base_fine, discount_amount, final_fine)


if __name__ == "__main__":
    main()