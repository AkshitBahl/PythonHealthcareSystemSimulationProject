"""
Simulation Mode
===============
Configures the simulation behaviour for Normal and Pandemic modes.
"""


class SimulationMode:
    """
    Represents the current operational mode of the healthcare simulation.

    In Normal mode: standard hospital operations, low infection rates.
    In Pandemic mode: heightened infection rates, surge capacity.

    Attributes:
        mode (str): Current mode — 'normal' or 'pandemic'.
        infection_rate (float): Base probability of infection per tick.
        recovery_rate (float): Base probability of recovery per tick.
        mortality_rate (float): Base mortality rate for infected patients.
        surge_capacity_multiplier (float): Multiplier for hospital bed capacity.
    """

    # Default parameters for each mode
    MODE_PARAMS = {
        "normal": {
            "infection_rate": 0.02,
            "recovery_rate": 0.15,
            "mortality_rate": 0.02,
            "surge_capacity_multiplier": 1.0,
        },
        "pandemic": {
            "infection_rate": 0.12,
            "recovery_rate": 0.08,
            "mortality_rate": 0.05,
            "surge_capacity_multiplier": 1.5,
        },
    }

    def __init__(self, mode: str = "normal"):
        self.mode: str = mode
        params = self.MODE_PARAMS[mode]
        self.infection_rate: float = params["infection_rate"]
        self.recovery_rate: float = params["recovery_rate"]
        self.mortality_rate: float = params["mortality_rate"]
        self.surge_capacity_multiplier: float = params["surge_capacity_multiplier"]

    @property
    def is_pandemic(self) -> bool:
        """Check if the current mode is Pandemic."""
        return self.mode == "pandemic"

    def toggle(self) -> str:
        """Toggle between normal and pandemic modes."""
        new_mode = "pandemic" if self.mode == "normal" else "normal"
        self.set_mode(new_mode)
        return self.mode

    def set_mode(self, mode: str) -> None:
        """Set the simulation mode and update all parameters."""
        if mode not in self.MODE_PARAMS:
            raise ValueError(f"Invalid mode: {mode}. Must be 'normal' or 'pandemic'.")

        self.mode = mode
        params = self.MODE_PARAMS[mode]
        self.infection_rate = params["infection_rate"]
        self.recovery_rate = params["recovery_rate"]
        self.mortality_rate = params["mortality_rate"]
        self.surge_capacity_multiplier = params["surge_capacity_multiplier"]

    def to_dict(self) -> dict:
        """Serialize the simulation mode to a dictionary."""
        return {
            "mode": self.mode,
            "is_pandemic": self.is_pandemic,
            "infection_rate": self.infection_rate,
            "recovery_rate": self.recovery_rate,
            "mortality_rate": self.mortality_rate,
            "surge_capacity_multiplier": self.surge_capacity_multiplier,
        }

    def __repr__(self) -> str:
        return f"SimulationMode(mode='{self.mode}', infection_rate={self.infection_rate})"
