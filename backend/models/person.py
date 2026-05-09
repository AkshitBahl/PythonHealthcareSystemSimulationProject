"""
Person Class Hierarchy
======================
Base class `Person` is extended into `Patient` and `Doctor`.

Demonstrates:
- Inheritance (Person → Patient, Doctor)
- Multiple instantiation (50+ Patients, 12 Doctors)
- List comprehension for filtering
- Encapsulation of health state logic

Health System:
- 3 statuses: Healthy, Infected, Deceased
- Treatment: doctor gives up to 2 treatments (+0.10 immunity each)
- If immunity > 0.50 after treatment → Healthy (immunity resets)
- If 2 treatments fail → Deceased
- Unadmitted infected patients die after 10 days
"""

import uuid
import random
from typing import Optional


class Person:
    """
    Base class representing any person in the healthcare system.

    Attributes:
        id (str): Unique identifier for the person.
        name (str): Full name.
        age (int): Age in years.
        gender (str): Gender ('Male', 'Female', 'Other').
        contact (str): Contact phone number.
    """

    def __init__(self, name: str, age: int, gender: str, contact: str = ""):
        self.id: str = str(uuid.uuid4())[:8]
        self.name: str = name
        self.age: int = age
        self.gender: str = gender
        self.contact: str = contact

    def get_info(self) -> dict:
        """Return a dictionary with the person's basic information."""
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "contact": self.contact,
        }

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', age={self.age})"


class Patient(Person):
    """
    A patient in the healthcare system. Extends Person with health-related
    attributes and methods for admission, discharge, and health updates.

    Attributes:
        health_status (str): Current status — 'Healthy', 'Infected', 'Deceased'.
        days_infected (int): Number of days the patient has been infected.
        assigned_facility (str | None): ID of the facility the patient is assigned to.
        assigned_doctor (str | None): ID of the assigned doctor.
        immunity (float): Immunity level 0.10 – 0.50 (determines treatment outcome).
        admitted (bool): Whether the patient is currently admitted to a facility.
        treatments_received (int): Number of treatments received for current infection.
    """

    # Three health statuses
    HEALTH_STATUSES = ["Healthy", "Infected", "Deceased"]

    # Treatment constants
    IMMUNITY_THRESHOLD = 0.50
    MAX_TREATMENTS = 2
    DAYS_UNTIL_DEATH_UNADMITTED = 10

    def __init__(self, name: str, age: int, gender: str, contact: str = ""):
        super().__init__(name, age, gender, contact)
        self.health_status: str = "Healthy"
        self.days_infected: int = 0
        self.assigned_facility: Optional[str] = None
        self.assigned_doctor: Optional[str] = None
        self.immunity: float = round(random.uniform(0.10, 0.50), 2)
        self.admitted: bool = False
        self.treatments_received: int = 0

    def admit(self, facility_id: str, doctor_id: str) -> None:
        """Admit the patient to a facility under a doctor's care."""
        self.admitted = True
        self.assigned_facility = facility_id
        self.assigned_doctor = doctor_id

    def discharge(self) -> None:
        """Discharge the patient from their current facility."""
        self.admitted = False
        self.assigned_facility = None
        self.assigned_doctor = None

    def infect(self) -> None:
        """Mark the patient as infected."""
        if self.health_status not in ("Infected", "Deceased"):
            self.health_status = "Infected"
            self.days_infected = 0
            self.treatments_received = 0

    def update_health(self, is_pandemic: bool = False) -> str:
        """
        Update the patient's health for the current simulation tick.

        - Deceased: no change.
        - Healthy: random chance of getting infected (higher in pandemic).
        - Infected + unadmitted: die after 10 days without treatment.
        - Infected + admitted: no change here (treatment handled by doctor).

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
            if random.random() < sick_chance:
                self.infect()

        return self.health_status

    def treat(self) -> str:
        """
        Apply one treatment to the patient.

        Each treatment: +0.10 immunity. If immunity exceeds threshold (0.50)
        the patient becomes Healthy (immunity resets). If 2 treatments fail
        to cross the threshold, the patient is Deceased.

        Returns:
            str: The updated health status after treatment.
        """
        if self.health_status != "Infected":
            return self.health_status

        self.treatments_received += 1
        self.immunity = round(self.immunity + 0.10, 2)

        if self.immunity > self.IMMUNITY_THRESHOLD:
            # Treatment succeeded — patient recovers
            self.health_status = "Healthy"
            self.days_infected = 0
            self.treatments_received = 0
            self.immunity = round(random.uniform(0.10, 0.50), 2)
        elif self.treatments_received >= self.MAX_TREATMENTS:
            # Two treatments failed — patient dies
            self.health_status = "Deceased"

        return self.health_status

    def to_dict(self) -> dict:
        """Serialize the patient to a dictionary for API responses."""
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
    A doctor in the healthcare system. Extends Person with medical
    specialization and patient management capabilities.

    Attributes:
        specialization (str): Medical specialization.
        assigned_facility (str | None): ID of the facility the doctor works at.
        assigned_patients (list[str]): List of patient IDs currently under care.
        max_patients (int): Maximum number of patients the doctor can handle.
        available (bool): Whether the doctor is currently available.
    """

    SPECIALIZATIONS = [
        "General Medicine", "Emergency Medicine", "Surgeon",
        "Pulmonologist", "Cardiologist", "Infectious Disease",
        "Pediatrics", "Oncology", "Neurologist", "ICU Specialist",
    ]

    def __init__(self, name: str, age: int, gender: str, specialization: str,
                 contact: str = ""):
        super().__init__(name, age, gender, contact)
        self.specialization: str = specialization
        self.assigned_facility: Optional[str] = None
        self.assigned_patients: list[str] = []
        self.max_patients: int = 8
        self.available: bool = True

    def assign_patient(self, patient_id: str) -> bool:
        """
        Assign a patient to this doctor.

        Returns:
            bool: True if assignment was successful, False if doctor is at capacity.
        """
        if len(self.assigned_patients) < self.max_patients:
            self.assigned_patients.append(patient_id)
            return True
        return False

    def remove_patient(self, patient_id: str) -> None:
        """Remove a patient from this doctor's care."""
        if patient_id in self.assigned_patients:
            self.assigned_patients.remove(patient_id)

    def diagnose(self, patient: "Patient") -> str:
        """
        Diagnose a patient based on their current health status.
        Uses list comprehension to assess symptoms.

        Returns:
            str: A diagnosis string.
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
        """Serialize the doctor to a dictionary for API responses."""
        info = self.get_info()
        info.update({
            "specialization": self.specialization,
            "assigned_facility": self.assigned_facility,
            "num_patients": len(self.assigned_patients),
            "max_patients": self.max_patients,
            "available": self.available,
        })
        return info
