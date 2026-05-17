import uuid     # To generate unique ids
import random   # We import this library in order to generate random values within a given range
from typing import List, Optional


class Person:
    """
    Base class representing person in the healthcare system.

    Attributes:
        id (str): Unique identifier for the person.
        name (str): Full name.
        age (int): Age in years.
        gender (str): Gender ('Male', 'Female', 'Other').
        contact (str): Contact phone number.
    """

    def __init__(self, name: str, age: int, gender: str, contact: str = ""):
        self.id: str = str(uuid.uuid4())[:8]   # Generates a big number, but we take the first 8
        self.name: str = name
        self.age: int = age
        self.gender: str = gender
        self.contact: str = contact

    def get_info(self) -> dict:
        """Return a dictionary with the person's info to send the data to our API"""
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "contact": self.contact,
        }


class Patient(Person):
    """
    A patient in the healthcare system. Extends Person and contain methods for admission, discharge, and health updates

    Attributes:
        health_status (str): Current status — 'Healthy', 'Infected', 'Deceased'
        immunity (float): Immunity level 0.0 – 0.5
        days_infected (int): No. of days the patient has been infected
        treatments_received (int): No. of treatments received
        recovered (bool): Whether the patient has recovered from a prior
            infection — grants strong resistance to reinfection
        admitted (bool): Whether the patient is admitted to a facility
        assigned_doctor (str): ID of the assigned doctor
        assigned_facility (str): ID of the facility the patient is assigned to
    """

    # Three health statuses
    HEALTH_STATUSES = ["Healthy", "Infected", "Deceased"]

    # Treatment constants
    IMMUNITY_THRESHOLD = 0.50
    MAX_TREATMENTS = 4
    DAYS_UNTIL_DEATH_UNADMITTED = 10

    # A recovered patient's reinfection chance is scaled by this factor
    # (0.05 = 95% less likely to be reinfected than a never-infected patient)
    RECOVERED_REINFECTION_FACTOR = 0.05

    def __init__(self, name: str, age: int, gender: str, contact: str = ""):
        super().__init__(name, age, gender, contact)
        self.health_status: str = "Healthy" # The patient starts out healthy
        self.immunity: float = round(random.uniform(0.1,0.5), 2)
        self.days_infected: int = 0
        self.treatments_received: int = 0
        self.recovered: bool = False
        self.admitted: bool = False
        self.assigned_doctor: Optional[str] = None
        self.assigned_facility: Optional[str] = None

    def admit(self, facility_id: str, doctor_id: str) -> None:
        """Admit the patient to a facility with a doctor"""
        self.admitted = True
        self.assigned_facility = facility_id
        self.assigned_doctor = doctor_id

    def infect(self) -> None:
        """Infect the patient"""
        if self.health_status is not ["Infected", "Deceased"]:
            self.health_status = "Infected"
            self.days_infected = 0
            self.treatments_received = 0

    def resists_infection(self) -> bool:
        """
        Decide whether the patient fends off an infection attempt.

        A patient who has recovered from a previous infection carries
        acquired immunity and resists reinfection the vast majority of the
        time. A patient who has never been infected never resists.

        Returns:
            bool: True if the infection attempt is resisted (no infection).
        """
        if not self.recovered:
            return False
        return random.random() >= self.RECOVERED_REINFECTION_FACTOR

    def update_health(self, is_pandemic: bool = False) -> str:
        """
        Update the patient's health status based on the simulation mode

        - Deceased: no change in patient's health status
        - Healthy: random chance of getting infected (higher in pandemic
          mode); recovered patients usually resist reinfection
        - Infected: In case of unadmitted, the patient die after 10 days without treatment
        In case of admitted, no change in patient's health status.

        Returns:
            str: The updated health status.
        """
        if self.health_status == "Deceased":
            return self.health_status

        if self.health_status == "Infected":
            self.days_infected += 1
            # Unadmitted infected patients die after 10 days
            if not self.admitted and self.days_infected >= self.DAYS_UNTIL_DEATH_UNADMITTED:
                self.health_status = "Deceased"

        elif self.health_status == "Healthy":
            sick_chance = 0.02 if not is_pandemic else 0.08
            if random.random() < sick_chance and not self.resists_infection():
                self.infect()

        return self.health_status

    def discharge(self) -> None:
        """Discharge the patient from the facility."""
        self.admitted = False
        self.assigned_facility = None
        self.assigned_doctor = None

    def treat(self) -> str:
        """
        Apply treatment to the patient

        Returns:
            str: The updated health status after treatment
        """
        if self.health_status != "Infected":
            return self.health_status

        self.treatments_received += 1
        self.immunity = round(self.immunity + 0.05, 2)

        if self.immunity > self.IMMUNITY_THRESHOLD:
            self.health_status = "Healthy"
            self.days_infected = 0
            self.treatments_received = 0
            self.immunity = round(random.uniform(0.10,0.80), 2)
            self.recovered = True
        elif self.treatments_received >= self.MAX_TREATMENTS:
            self.health_status = "Deceased"

        return self.health_status

    def to_dict(self) -> dict:
        """Return a dictionary with the patient's info to send the data to our API"""
        info = self.get_info()
        info.update({
            "health_status": self.health_status,
            "days_infected": self.days_infected,
            "admitted": self.admitted,
            "assigned_facility": self.assigned_facility,
            "assigned_doctor": self.assigned_doctor,
            "immunity": self.immunity,
            "treatments_received": self.treatments_received,
        })
        return info

class Doctor(Person):
    """
    A doctor in the healthcare system. Extends Person and manages patients

    Attributes:
        assigned_facility (str | None): ID of the facility the doctor works at.
        assigned_patients (list[str]): List of patient IDs currently under care.
        base_max_patients (int): Original max patient capacity (before surge).
        max_patients (int): Maximum number of patients the doctor can handle.
        available (bool): Whether the doctor is currently available.
    """
    def __init__(self, name: str, age: int, gender: str, contact: str = ""):
        super().__init__(name, age, gender, contact)
        self.assigned_patients: list[str] = []
        self.base_max_patients: int = 8
        self.max_patients: int = self.base_max_patients
        self.assigned_facility: Optional[str] = None
        self.available: bool = True

    def assign_patient(self, patient_id: str) -> bool:
        """
        Assign a patient to the doctor

        Returns:
            bool: True if doctor assigned to the patient otherwise False
        """
        if len(self.assigned_patients) < self.max_patients:
            self.assigned_patients.append(patient_id)
            return True
        return False

    def remove_patient(self, patient_id:str) -> bool:
        """Remove a patient from the doctor assigned lists"""
        if patient_id in self.assigned_patients:
            self.assigned_patients.remove(patient_id)
            return True
        return False

    def apply_surge_capacity(self, multiplier: float) -> None:
        """
        In pandemic mode, the doctor's max patient capacity is scaled up
        by the surge capacity multiplier.
        """
        self.max_patients = int(self.base_max_patients * multiplier)

    def diagnose(self, patient: "Patient") -> str:
        """
        Diagnose the patient

        Returns:
            str: diagnosed patient string
        """

        # List comprehension: gather relevant conditions
        conditions = [
            status for status in Patient.HEALTH_STATUSES
            if status == patient.health_status
        ]
        diagnosis = f"Patient {patient.name} diagnosed: {patient.health_status}"
        if patient.health_status == "Infected":
            diagnosis += " (Infectious disease detected)"
        return diagnosis

    def to_dict(self) -> dict:
        """Return a dictionary with the doctor's info to send the data to our API"""
        info = self.get_info()
        info.update({
            "assigned_facility": self.assigned_facility,
            "num_patients": len(self.assigned_patients),
            "max_patients": self.max_patients,
            "available": self.available,
        })
        return info
