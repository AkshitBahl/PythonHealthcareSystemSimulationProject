import uuid # To generate unique ids for all people
# from typing import Optional

class Facility:
    """
    Base class representing medical facility infrastructure

    Attributes:
        id (str): Unique facility ID
        name (str): Facility name
        location (str): location
        facility_type (str): Type of facility ('Hospital', 'Pharmacy')
        active (bool): Whether the facility is currently active
    """

    def __init__(self, name: str, location: str, facility_type: str):
        self.id: str = str(uuid.uuid4())[:8]
        self.name: str = name
        self.location: str = location
        self.facility_type: str = facility_type
        self.active: bool = True

    def get_status(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "facility_type": self.facility_type,
            "active": self.active,
        }

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', location='{self.location}')"


class Hospital(Facility):
    """
    A hospital facility for management of beds, doctors and patients.

    Attributes:
        total_beds (int): Total no. of beds
        base_beds (int): Original bed count (before surge capacity)
        doctors (list[str]): List of doctor IDs assigned to the hospital
        patients (list[str]): List of admitted patient IDs in the hospital
    """

    def __init__(self, name: str, location: str, total_beds: int = 100):
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
            float: Occupancy rate as a percentage (0-100).
        """
        return round((self.occupied_beds / self.total_beds) * 100, 1)

    def admit_patient(self, patient_id: str) -> bool:
        """
        Admit a patient to the hospital.

        Returns:
            bool: True if admission was successful.
        """
        if self.available_beds > 0:
            self.patients.append(patient_id)
            return True
        return False

    def discharge_patient(self, patient_id: str) -> bool:
        """
        Discharge a patient from hospital

        Returns:
            bool: True if patient was found and discharged.
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
    A pharmacy facility with a dictionary for medication inventory

    Attributes:
        inventory (dict): It maps medication names with the stock amounts
        prescriptions_filled (int): Total prescriptions filled
        daily_prescriptions (int): Prescriptions filled today
    """

    def __init__(self, name: str, location: str):
        super().__init__(name, location, facility_type="Pharmacy")
        self.prescriptions_filled: int = 0
        self.daily_prescriptions: int = 0
        self.inventory: dict[str, int] = {
            "Paracetamol": 500,
            "Amoxicillin": 200,
            "Ibuprofen": 400,
            "Dexamethasone": 300,
            "Remdesivir": 50,
            "Aspirin": 350,
            "COVID Vaccine": 100,
            "Oseltamivir": 80,
        }

    def fill_prescription(self, medication_name: str, quantity: int = 1) -> bool:
        """
        Fill a prescription by dispensing medication from stock.

        Returns:
            bool: True if medication was available and dispensed.
        """
        if medication_name in self.inventory and self.inventory[medication_name] >= quantity:
            self.inventory[medication_name] -= quantity
            self.prescriptions_filled += 1
            self.daily_prescriptions += 1
            return True
        return False

    def reset_daily_count(self) -> None:
        """Reset the daily prescription counter."""
        self.daily_prescriptions = 0

    def to_dict(self) -> dict:
        """Convert the pharmacy object to a dictionary form for API responses."""
        status = self.get_status()

        # List comprehension: format inventory as a list of dicts for the frontend
        inventory_list = [{"name": k, "stock": v} for k, v in self.inventory.items()]

        status.update({
            "inventory": inventory_list,
            "prescriptions_filled": self.prescriptions_filled,
            "daily_prescriptions": self.daily_prescriptions,
        })
        return status
