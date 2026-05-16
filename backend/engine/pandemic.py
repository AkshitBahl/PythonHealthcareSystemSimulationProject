import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.models.simulation_mode import SimulationMode

class PandemicEngine:
    """
    Manages pandemic-specific logic. One tick represents one day

    Attributes:
        total_infections (int): Total infections
        total_deaths (int): Total deaths
        daily_new_infections (int): New infections on that specific day
        daily_new_deaths (int): New deaths on that specific day
    """

    def __init__(self):
        self.total_infections: int = 0
        self.total_deaths: int = 0
        self.daily_new_infections: int = 0
        self.daily_new_deaths: int = 0

    def seed_infection(self, patients: list, count: int = 5) -> list[str]:
        """
        Selects random healthy patients to infect

        Returns:
            list[str]: IDs of the new infected patients
        """
        # List comprehension: Find healthy patients
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
        Simulate one tick of infection spread

        Returns:
            dict: Returns the summary of spread results for this tick.
        """
        self.daily_new_infections = 0
        self.daily_new_deaths = 0

        # filter() to get susceptible patients which are healthy
        susceptible = list(filter(
            lambda p: p.health_status == "Healthy",
            patients
        ))

        # Population-level infection: Infect  15% of healthy patients
        num_to_infect = round(len(susceptible) * mode.infection_rate)
        if num_to_infect > 0 and susceptible:
            to_infect = random.sample(
                susceptible, min(num_to_infect, len(susceptible))
            )
            for contact in to_infect:
                contact.infect()
                self.daily_new_infections += 1
                self.total_infections += 1

        # Update health for all patients
        previous_statuses = {p.id: p.health_status for p in patients}
        list(map(lambda p: p.update_health(is_pandemic=mode.is_pandemic), patients))

        # Count deaths by checking the status changes
        for patient in patients:
            prev = previous_statuses.get(patient.id)
            if prev != "Deceased" and patient.health_status == "Deceased":
                self.daily_new_deaths += 1
                self.total_deaths += 1

        return self._get_tick_summary(patients)

    def get_sir_counts(self, patients: list) -> dict:
        """
        Calculate current health

        Returns:
            dict: Counts for healthy, infected, deceased compartments.
        """
        healthy = len([p for p in patients if p.health_status == "Healthy"])
        infected = len([p for p in patients if p.health_status == "Infected"])
        deceased = len([p for p in patients if p.health_status == "Deceased"])

        return {
            "healthy": healthy,
            "infected": infected,
            "deceased": deceased,
            "total": len(patients),
        }

    def _get_tick_summary(self, patients: list) -> dict:
        """Generate a summary for the current tick"""
        sir = self.get_sir_counts(patients)
        return {
            "sir": sir,
            "daily_new_infections": self.daily_new_infections,
            "daily_new_deaths": self.daily_new_deaths,
            "total_infections": self.total_infections,
            "total_deaths": self.total_deaths,
        }

    def reset(self) -> None:
        """Reset all the pandemic related counters"""
        self.total_infections = 0
        self.total_deaths = 0
        self.daily_new_infections = 0
        self.daily_new_deaths = 0

    def to_dict(self) -> dict:
        """Convert the SimulationMode object to a dictionary form for API responses"""
        return {
            "total_infections": self.total_infections,
            "total_deaths": self.total_deaths,
            "daily_new_infections": self.daily_new_infections,
            "daily_new_deaths": self.daily_new_deaths,
        }
