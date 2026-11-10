import datetime
import pytest
from calculator import (
    calculate_days_late,
    calculate_fine,
    get_item_type,
    get_member_type,
    main,
    print_fine_summary,
)


# --- Core Logic Tests ---

def test_calculate_days_late_positive():
    due = datetime.date(2026, 8, 1)
    ret = datetime.date(2026, 8, 27)
    assert calculate_days_late(due, ret) == 26


def test_calculate_days_late_early_or_on_time():
    due = datetime.date(2026, 8, 27)
    ret = datetime.date(2026, 8, 20)
    assert calculate_days_late(due, ret) == 0


def test_calculate_fine_standard_adult():
    base, discount, final = calculate_fine(10, "Standard", "Adult")
    assert base == 5.00
    assert discount == 0.00
    assert final == 5.00


def test_calculate_fine_bestseller_student():
    base, discount, final = calculate_fine(5, "Best-Seller", "Student")
    assert base == 5.00
    assert discount == 1.00
    assert final == 4.00


def test_calculate_fine_dvd_senior():
    base, discount, final = calculate_fine(10, "DVD", "Senior")
    assert base == 20.00
    assert discount == 10.00
    assert final == 10.00


def test_calculate_fine_max_cap():
    base, discount, final = calculate_fine(50, "DVD", "Adult")
    assert base == 100.00
    assert discount == 0.00
    assert final == 15.00


# --- Interactive Input Function Tests ---

@pytest.mark.parametrize(
    "user_input, expected",
    [
        ("1", "Adult"),
        ("2", "Student"),
        ("3", "Senior"),
        ("99", "Adult"),  # default fallback
    ],
)
def test_get_member_type(monkeypatch, user_input, expected):
    monkeypatch.setattr("builtins.input", lambda _: user_input)
    assert get_member_type() == expected


@pytest.mark.parametrize(
    "user_input, expected",
    [
        ("1", "Standard"),
        ("2", "Best-Seller"),
        ("3", "DVD"),
        ("99", "Standard"),  # default fallback
    ],
)
def test_get_item_type(monkeypatch, user_input, expected):
    monkeypatch.setattr("builtins.input", lambda _: user_input)
    assert get_item_type() == expected


# --- Console Output & Main Routine Tests ---

def test_print_fine_summary(capsys):
    print_fine_summary(10, 5.0, 0.0, 5.0)
    captured = capsys.readouterr()
    assert "Days Late: 10" in captured.out
    assert "Base Fine: $5.00" in captured.out
    assert "Final Fine: $5.00" in captured.out


def test_main_valid_workflow(monkeypatch, capsys):
    user_inputs = iter(["1", "1", "2026-08-01", "2026-08-11"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

    main()

    captured = capsys.readouterr()
    assert "Days Late: 10" in captured.out
    assert "Final Fine: $5.00" in captured.out


def test_main_invalid_date_format(monkeypatch, capsys):
    user_inputs = iter(["1", "1", "invalid-date", "2026-08-11"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()
    assert "Invalid date format." in captured.out