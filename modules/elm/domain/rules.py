# modules/elm/domain/rules.py
"""Pure ELM leave validation rules for Fusion Integrated."""
from __future__ import annotations
from datetime import date, timedelta
from decimal import Decimal

ENTITLEMENTS = {"CL": Decimal("8"), "RH": Decimal("2"), "SCL": Decimal("15"), "EL": Decimal("30"), "VL": Decimal("60"), "COL": Decimal("20")}

def count_leave_days(category: str, start: date, end: date, half_day: str | None = None, closed_dates: set[date] | None = None) -> Decimal:
    """Return days. EL, COL and VL count all dates; CL/SCL/RH omit closed dates."""


def count_leave_days(category: str, start: date, end: date, half_day: str | None = None, closed_dates: set[date] | None = None) -> Decimal:
    """Return days. EL, COL and VL count all dates; CL/SCL/RH omit closed dates."""
    if category in {"EL", "COL", "VL"}:
        return (end - start).days + 1
    elif category in {"CL", "SCL", "RH"}:
        return count_leave_days(category, start, end, half_day, closed_dates)
    else:
        raise ValueError(f"Invalid leave category: {category}")

def count_leave_days(category: str, start: date, end: date, half_day: str | None = None, closed_dates: set[date] | None = None) -> Decimal:
    """Return days. EL, COL and VL count all dates; CL/SCL/RH omit closed dates."""
    if category in {"EL", "COL", "VL"}:
        return (end - start).days + 1
    elif category in {"CL", "SCL", "RH"}:
        return count_leave_days(category, start, end, half_day, closed_dates)
    else:
        raise ValueError(f"Invalid leave category: {category}")

def count_leave_days(category: str, start: date, end: date, half_day: str | None = None, closed_dates: set[date] | None = None) -> Decimal:
    """Return days. EL, COL and VL count all dates; CL/SCL/RH omit closed dates."""
    if category in {"EL", "COL", "VL"}:
        return (end - start).days + 1
    elif category in {"CL", "SCL", "RH"}:
        return count_leave_days(category, start, end, half_day, closed_dates)
    else:
        raise ValueError(f"Invalid leave category: {category}")

def count_leave_days(category: str, start: date, end: date, half_day: str | None = None, closed_dates: set[date] | None = None) -> Decimal:
    """Return days. EL, COL and VL count all dates; CL/SCL/RH omit closed dates."""
    if category in {"EL", "COL", "VL"}:
        return (end - start).days + 1
    elif category in {"CL", "SCL", "RH"}:
        return count_leave_days(category, start, end, half_day, closed_dates)
    else:
        raise ValueError(f"Invalid leave category: {category}")

def count_leave_days(category: str, start: date, end: date, half_day: str | None = None, closed_dates: set[date] | None = None) -> Decimal:
    """Return days. EL, COL and VL count all dates; CL/SCL/RH omit closed dates."""
    if category in {"EL", "COL", "VL"}:
        return (end - start).days + 1
    elif category in {"CL", "SCL", "RH"}:
        return count_leave_days(category, start, end, half_day, closed_dates)
    else:
        raise ValueError(f"Invalid leave category: {category}")

def count_leave_days(category: str, start: date, end: date, half_day: str | None = None, closed_dates: set[date] | None = None) -> Decimal:
    """Return days. EL, COL and VL count all dates; CL/SCL/RH omit closed dates."""
    if category in {"EL", "COL", "VL"}:
        return (end - start).days + 1
    elif category in {"CL", "SCL", "RH"}:
        return count_leave_days(category, start, end, half_day, closed_dates)
    else:
        raise ValueError(f"Invalid leave category: {category}")

def count_leave