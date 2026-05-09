"""
Statistics Collector
====================
Collects and aggregates simulation metrics over time for visualization.

Demonstrates:
- reduce() for aggregating metrics across facilities
- List comprehension for time-series data construction
- map() for transforming data for API responses
"""

from functools import reduce
from typing import Any


class StatisticsCollector:
    """
    Collects daily simulation metrics and maintains time-series data
    for the dashboard charts.

    Attributes:
        daily_records (list[dict]): List of daily snapshots.
        current_day (int): Current simulation day.
    """

    def __init__(self):
        self.daily_records: list[dict] = []
        self.current_day: int = 0

    def record_day(self, day: int, patients: list, hospitals: list,
                   pharmacies: list, mode_data: dict,
                   pandemic_data: dict | None = None) -> dict:
        """
        Record a full snapshot of the simulation state for one day.

        Uses reduce() to aggregate metrics across all hospitals,
        and list comprehension / map() for data transformation.
        """
        self.current_day = day

        # --- Patient statistics using list comprehension ---
        total_patients = len(patients)
        # List comprehension to count each health status
        status_counts = {
            status: len([p for p in patients if p.health_status == status])
            for status in ["Healthy", "Infected", "Deceased"]
        }
        infected_count = len([p for p in patients if p.health_status == "Infected"])
        admitted_count = len([p for p in patients if p.admitted])

        # --- Hospital statistics using reduce() ---
        # reduce() to sum total beds across all hospitals
        total_beds = reduce(
            lambda acc, h: acc + h.total_beds,
            hospitals, 0
        )
        # reduce() to sum occupied beds across all hospitals
        occupied_beds = reduce(
            lambda acc, h: acc + h.occupied_beds,
            hospitals, 0
        )

        occupancy_rate = round((occupied_beds / total_beds * 100), 1) if total_beds > 0 else 0.0

        # --- Pharmacy statistics using map() and reduce() ---
        # map() to extract total stock from each pharmacy
        pharmacy_stocks = list(map(
            lambda ph: sum(ph.inventory.values()),
            pharmacies
        ))
        total_pharmacy_stock = reduce(lambda a, b: a + b, pharmacy_stocks, 0)

        # map() to get low stock count from each pharmacy
        low_stock_counts = list(map(
            lambda ph: len([stock for stock in ph.inventory.values() if stock < 20]),
            pharmacies
        ))
        total_low_stock = reduce(lambda a, b: a + b, low_stock_counts, 0)

        # map() to get prescriptions filled
        prescriptions_filled = list(map(
            lambda ph: ph.prescriptions_filled,
            pharmacies
        ))
        total_prescriptions = reduce(lambda a, b: a + b, prescriptions_filled, 0)

        # --- Build the daily record ---
        record = {
            "day": day,
            "mode": mode_data.get("mode", "normal"),
            "patients": {
                "total": total_patients,
                "status_counts": status_counts,
                "infected": infected_count,
                "admitted": admitted_count,
            },
            "hospitals": {
                "total_beds": total_beds,
                "occupied_beds": occupied_beds,
                "occupancy_rate": occupancy_rate,
            },
            "pharmacy": {
                "total_stock": total_pharmacy_stock,
                "low_stock_alerts": total_low_stock,
                "prescriptions_filled": total_prescriptions,
            },
        }

        # Add pandemic data if available
        if pandemic_data:
            record["pandemic"] = pandemic_data

        self.daily_records.append(record)
        return record

    def get_time_series(self, metric_path: str) -> list[dict]:
        """
        Extract a time-series for a specific metric from daily records.
        Uses list comprehension to build the series.
        """
        keys = metric_path.split(".")

        def extract_value(record: dict) -> Any:
            """Navigate nested dict by dot path."""
            val = record
            for key in keys:
                if isinstance(val, dict) and key in val:
                    val = val[key]
                else:
                    return None
            return val

        # List comprehension to build time series
        return [
            {"day": record["day"], "value": extract_value(record)}
            for record in self.daily_records
            if extract_value(record) is not None
        ]

    def get_latest(self) -> dict | None:
        """Get the most recent daily record."""
        return self.daily_records[-1] if self.daily_records else None

    def get_summary(self) -> dict:
        """Get a summary of all collected statistics."""
        return {
            "current_day": self.current_day,
            "total_records": len(self.daily_records),
            "latest": self.get_latest(),
        }

    def get_all_records(self) -> list[dict]:
        """Get all daily records for chart data."""
        return self.daily_records

    def reset(self) -> None:
        """Reset all statistics."""
        self.daily_records = []
        self.current_day = 0
