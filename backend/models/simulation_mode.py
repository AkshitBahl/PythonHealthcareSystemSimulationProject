class SimulationMode:
    """
    Represents the operational mode of the healthcare simulation.

    In Normal mode: basic hospital operations
    In Pandemic mode: increased infection rate

    Attributes:
        mode (str): Current mode — 'normal' or 'pandemic'.
        infection_rate (float): Base probability of infection per tick.
        surge_capacity_multiplier (float): Multiplier for hospital bed capacity.
    """

    # Default parameters for each mode
    MODE_PARAMS = {
        "normal": {
            "infection_rate": 0.02,
            "surge_capacity_multiplier": 1.0,
        },
        "pandemic": {
            "infection_rate": 0.15,
            "surge_capacity_multiplier": 1.5,
        },
    }

    def __init__(self, mode: str = "normal"):
        self.mode: str = mode
        params = self.MODE_PARAMS[mode]
        self.infection_rate: float = params["infection_rate"]
        self.surge_capacity_multiplier: float = params["surge_capacity_multiplier"]

    # @property  # Allows a method to be accessed like a read-only attribute
    @property
    def is_pandemic(self) -> bool:
        """Check if the current mode is Pandemic"""
        return self.mode == "pandemic"

    def toggle(self) -> str:
        """To switch between normal and pandemic modes"""
        new_mode = "pandemic" if self.mode == "normal" else "normal"
        self.set_mode(new_mode)
        return self.mode

    def set_mode(self, mode: str) -> None:
        """Set the simulation mode"""
        if mode not in self.MODE_PARAMS:
            raise ValueError(f"Invalid mode: {mode}. Must be 'normal' or 'pandemic'.")

        self.mode = mode
        params = self.MODE_PARAMS[mode]
        self.infection_rate = params["infection_rate"]
        self.surge_capacity_multiplier = params["surge_capacity_multiplier"]

    def to_dict(self) -> dict:
        """Convert the SimulationMode object to a dictionary form for API responses"""
        return {
            "mode": self.mode,
            "is_pandemic": self.is_pandemic,
            "infection_rate": self.infection_rate,
            "surge_capacity_multiplier": self.surge_capacity_multiplier,
        }
