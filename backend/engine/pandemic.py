"""
Pandemic Engine — SIR Model
============================
Implements a Susceptible-Infected-Recovered (SIR) epidemiological model
for simulating disease spread during pandemic mode.

Demonstrates:
- List comprehension for population state tracking
- filter() for identifying susceptible/infected populations
- map() for applying infection state changes
"""

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.models.person import Patient
    from backend.models.simulation_mode import SimulationMode


class PandemicEngine:
    """
    Manages pandemic-specific logic including infection spread,
    recovery tracking, and SIR model calculations.

    Attributes:
        total_infections (int): Cumulative total infections.
        total_recoveries (int): Cumulative total recoveries.
        total_deaths (int): Cumulative total deaths.
        daily_new_infections (int): New infections in the current tick.
        daily_new_recoveries (int): New recoveries in the current tick.
        daily_new_deaths (int): New deaths in the current tick.
    """

    def __init__(self):
        self.total_infections: int = 0
        self.total_recoveries: int = 0
        self.total_deaths: int = 0
        self.daily_new_infections: int = 0
        self.daily_new_recoveries: int = 0
        self.daily_new_deaths: int = 0

    def seed_infection(self, patients: list, count: int = 5) -> list[str]:
        """
        Seed initial infections when pandemic mode is activated.
        Selects random healthy patients to infect.

        Returns:
            list[str]: IDs of newly infected patients.
        """
        # List comprehension: find healthy patients
        susceptible = [p for p in patients if p.health_status == "Healthy"]

        to_infect = random.sample(susceptible, min(count, len(susceptible)))
        infected_ids = []

        for patient in to_infect:
            patient.infect()
            self.total_infections += 1
            infected_ids.append(patient.id)

        return infected_ids

    def spread_infection(self, patients: list, mode: "SimulationMode") -> dict:
        """
        Simulate one tick of infection spread using SIR dynamics.

        Uses:
        - filter() to identify susceptible populations
        - map() for batch status updates

        Returns:
            dict: Summary of spread results for this tick.
        """
        self.daily_new_infections = 0
        self.daily_new_recoveries = 0
        self.daily_new_deaths = 0

        # filter() to get susceptible patients (healthy, not deceased)
        susceptible = list(filter(
            lambda p: p.health_status == "Healthy",
            patients
        ))

        # Infection spread: each susceptible has a chance of getting infected
        for contact in susceptible:
            infection_prob = mode.infection_rate * (1 - contact.immunity)
            if random.random() < infection_prob:
                contact.infect()
                self.daily_new_infections += 1
                self.total_infections += 1

        # Health updates for all patients (uses map)
        previous_statuses = {p.id: p.health_status for p in patients}
        list(map(lambda p: p.update_health(is_pandemic=mode.is_pandemic), patients))

        # Count recoveries and deaths from status changes
        for patient in patients:
            prev = previous_statuses.get(patient.id)
            if prev != "Recovered" and patient.health_status == "Recovered":
                self.daily_new_recoveries += 1
                self.total_recoveries += 1
            elif prev != "Deceased" and patient.health_status == "Deceased":
                self.daily_new_deaths += 1
                self.total_deaths += 1

        return self._get_tick_summary(patients)

    def get_sir_counts(self, patients: list) -> dict:
        """
        Calculate current SIR compartment counts.
        Uses list comprehension for categorization.

        Returns:
            dict: Counts for S, I, R compartments.
        """
        susceptible = len([p for p in patients if p.health_status == "Healthy"])
        infected = len([p for p in patients if p.health_status == "Infected"])
        recovered = len([p for p in patients if p.health_status == "Recovered"])
        deceased = len([p for p in patients if p.health_status == "Deceased"])

        return {
            "susceptible": susceptible,
            "infected": infected,
            "recovered": recovered,
            "deceased": deceased,
            "total": len(patients),
        }

    def _get_tick_summary(self, patients: list) -> dict:
        """Generate a summary for the current tick."""
        sir = self.get_sir_counts(patients)
        return {
            "sir": sir,
            "daily_new_infections": self.daily_new_infections,
            "daily_new_recoveries": self.daily_new_recoveries,
            "daily_new_deaths": self.daily_new_deaths,
            "total_infections": self.total_infections,
            "total_recoveries": self.total_recoveries,
            "total_deaths": self.total_deaths,
        }

    def reset(self) -> None:
        """Reset all pandemic tracking counters."""
        self.total_infections = 0
        self.total_recoveries = 0
        self.total_deaths = 0
        self.daily_new_infections = 0
        self.daily_new_recoveries = 0
        self.daily_new_deaths = 0

    def to_dict(self) -> dict:
        """Serialize the pandemic engine state."""
        return {
            "total_infections": self.total_infections,
            "total_recoveries": self.total_recoveries,
            "total_deaths": self.total_deaths,
            "daily_new_infections": self.daily_new_infections,
            "daily_new_recoveries": self.daily_new_recoveries,
            "daily_new_deaths": self.daily_new_deaths,
        }
