import uuid     # To generate unique ids

class Facility:
    """
    Base class representing medical facility

    Attributes:
        id (str): ID of the facility
        name (str): Name of the facility
        location (str): Location of the facility
        facility_type (str): Type of facility ('Hospital', 'Pharmacy')
        active (bool): Where the facility is active
    """

    def __init__(self, name: str, location: str, facility_type: str):
        self.id: str = str(uuid.uuid4())[:8]
        self.name: str = name
        self.location: str = location
        self.facility_type: str = facility_type
        self.active: bool = True

    def get_status(self) -> dict:
        """Convert the Facility object to a dictionary form for API responses"""
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "facility_type": self.facility_type,
            "active": self.active,
        }

class Hospital(Facility):
    """
    A hospital facility for management of beds, doctors and patients

    Attributes:
        total_beds (int): Total no. of beds
        base_beds (int): Original bed count
        doctors (list[str]): List of doctor IDs assigned to the hospital
        patients (list[str]): List of admitted patient IDs in the hospital
    """

    def __init__(self, name: str, location: str, total_beds: int = 10):
        super().__init__(name, location, facility_type="Hospital")
        self.total_beds: int = total_beds
        self.base_beds: int = total_beds
        self.doctors: list[str] = []
        self.patients: list[str] = []

    # @property -> # Allows a method to be accessed like a read-only attribute
    @property
    def occupied_beds(self) -> int:
        return len(self.patients)

    @property
    def available_beds(self) -> int:
        return max(0, self.total_beds - self.occupied_beds)

    def get_occupancy_rate(self) -> float:
        """
        Calculate the bed occupancy rate

        Returns:
            float: Returns occupancy rate as a percentage
        """
        return round((self.occupied_beds / self.total_beds) * 100, 1)

    def admit_patient(self, patient_id: str) -> bool:
        """
        Admit a patient to the hospital

        Returns:
            bool: True if patient is admitted
        """
        if self.available_beds > 0:
            self.patients.append(patient_id)
            return True
        return False

    def discharge_patient(self, patient_id: str) -> bool:
        """
        Discharge a patient from hospital

        Returns:
            bool: True if patient was found and discharged
        """
        if patient_id in self.patients:
            self.patients.remove(patient_id)
            return True
        return False

    def apply_surge_capacity(self, multiplier: float) -> None:
        """
        In pandemic mode, beds are increased up by the surge capacity multiplier
        """
        self.total_beds = int(self.base_beds * multiplier)

    def to_dict(self) -> dict:
        """Convert the hospital object to a dictionary form for API responses"""
        status = self.get_status()
        status.update({
            "total_beds": self.total_beds,
            "occupied_beds": self.occupied_beds,
            "available_beds": self.available_beds,
            "occupancy_rate": self.get_occupancy_rate(),
            "num_doctors": len(self.doctors),
            "num_patients": len(self.patients),
        })
        return status


class Pharmacy(Facility):
    """
    A pharmacy facility for medicine inventory

    Attributes:
        inventory (dict): It maps medicine names with the available amount
        prescriptions_filled (int): Total prescriptions filled
        daily_prescriptions (int): Prescriptions filled today
    """

    def __init__(self, name: str, location: str):
        super().__init__(name, location, facility_type="Pharmacy")
        self.prescriptions_filled: int = 0
        self.daily_prescriptions: int = 0
        self.inventory: dict[str, int] = {
            "Paracetamol": 100,
        }

    def fill_prescription(self, medication_name: str, quantity: int = 1) -> bool:
        """
        Give medicine from stock

        Returns:
            bool: True if medicine has been given
        """
        if medication_name in self.inventory and self.inventory[medication_name] >= quantity:
            self.inventory[medication_name] -= quantity
            self.prescriptions_filled += 1
            self.daily_prescriptions += 1
            return True
        return False

    def reset_daily_count(self) -> None:
        """Reset the daily prescription counter"""
        self.daily_prescriptions = 0

    def to_dict(self) -> dict:
        """Convert the pharmacy object to a dictionary form for API responses"""
        status = self.get_status()

        # List comprehension: format the inventory as a list of dictionary for the frontend
        inventory_list = [{"name": k, "stock": v} for k, v in self.inventory.items()]

        status.update({
            "inventory": inventory_list,
            "prescriptions_filled": self.prescriptions_filled,
            "daily_prescriptions": self.daily_prescriptions,
        })
        return status
