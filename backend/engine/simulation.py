import random
from functools import reduce

from backend.models.person import Patient, Doctor
from backend.models.facility import Hospital, Pharmacy
from backend.models.simulation_mode import SimulationMode

# --- Name data to generate the population/patient ---
FIRST_NAMES_MALE = [
    "James", "Robert", "John", "Michael", "David", "William", "Richard",
    "Joseph", "Thomas", "Christopher", "Daniel", "Matthew", "Anthony",
    "Mark", "Steven", "Andrew", "Paul", "Joshua", "Kenneth", "Kevin",
]
FIRST_NAMES_FEMALE = [
    "Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth",
    "Susan", "Jessica", "Sarah", "Karen", "Lisa", "Nancy", "Betty",
    "Margaret", "Sandra", "Ashley", "Dorothy", "Kimberly", "Emily",
    "Donna",
]
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
]

# Medicine mapping
MEDICATIONS = ["Paracetamol"]


class HealthcareSimulation:
    """
    The simulation engine managing the healthcare network

    Creates a population of patients, doctors, and facilities.
    Runs daily 'ticks' that simulate health changes, admissions, discharges,
    prescriptions, and (in pandemic mode) infection spread.

    Attributes:
        day (int): Current simulation day.
        mode (SimulationMode): Active simulation mode (Normal/Pandemic).
        patients (list[Patient]): All patients in the simulation.
        doctors (list[Doctor]): All doctors in the simulation.
        hospitals (list[Hospital]): All hospitals.
        pharmacies (list[Pharmacy]): All pharmacies.
        total_infections (int): Cumulative infections since the last reset.
        total_deaths (int): Cumulative deaths since the last reset.
        daily_new_infections (int): New infections recorded on the current day.
        daily_new_deaths (int): New deaths recorded on the current day.
    """

    def __init__(self, num_patients: int = 50):
        self.num_patients: int = num_patients
        self.day: int = 0
        self.mode: SimulationMode = SimulationMode("normal")

        # --- Infection tracking counters ---
        self.total_infections: int = 0
        self.total_deaths: int = 0
        self.daily_new_infections: int = 0
        self.daily_new_deaths: int = 0

        # --- Multiple instantiation: Generate population ---
        self.patients: list[Patient] = self._generate_patients(num_patients)
        self.doctors: list[Doctor] = self._generate_doctors(12)

        # --- Create facilities ---
        self.hospitals: list[Hospital] = [
            Hospital("City General Hospital", "Downtown", total_beds=6),
            Hospital("St. Mary's Medical Center", "Westside", total_beds=8),
            Hospital("University Teaching Hospital", "Northgate", total_beds=5),
        ]
        self.pharmacies: list[Pharmacy] = [
            Pharmacy("Central Pharmacy", "Downtown"),
            Pharmacy("HealthPlus Pharmacy", "Eastside"),
        ]

        # --- Assign doctors to facilities ---
        self._assign_staff_to_facilities()

    def _generate_patients(self, count: int) -> list[Patient]:
        """
        Generate a population of patients with random demographics.
        Uses list comprehension for batch creation.
        """
        patients = []
        for _ in range(count):
            gender = random.choice(["Male", "Female"])
            if gender == "Male":
                first = random.choice(FIRST_NAMES_MALE)
            else:
                first = random.choice(FIRST_NAMES_FEMALE)
            last = random.choice(LAST_NAMES)
            name = f"{first} {last}"
            age = random.randint(5, 85)
            contact = f"+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
            patients.append(Patient(name, age, gender, contact))
        return patients

    def _generate_doctors(self, count: int) -> list[Doctor]:
        """
        Generate doctors.
        Demonstrates multiple instantiation of Doctor class.
        """
        doctors = []
        for i in range(count):
            gender = random.choice(["Male", "Female"])
            if gender == "Male":
                first = random.choice(FIRST_NAMES_MALE)
            else:
                first = random.choice(FIRST_NAMES_FEMALE)
            last = random.choice(LAST_NAMES)
            name = f"Dr. {first} {last}"
            age = random.randint(30, 65)
            doctors.append(Doctor(name, age, gender))
        return doctors

    def _assign_staff_to_facilities(self) -> None:
        """Distribute doctors across hospitals (round-robin)."""
        for i, doctor in enumerate(self.doctors):
            hospital = self.hospitals[i % len(self.hospitals)]
            doctor.assigned_facility = hospital.id
            hospital.doctors.append(doctor.id)

    def tick(self) -> dict:
        """
        Advance the simulation by one day.

        The same pipeline runs for both modes:
        1. Spread infection and update every patient's health (map())
        2. Admit infected patients who need a bed (using filter())
        3. Treat admitted infected patients (doctor + pharmacy)
        4. Discharge healthy/deceased patients (using filter())
        5. Record statistics and return a snapshot

        Normal and Pandemic modes differ only in the infection rate and
        the surge capacity applied to hospital beds and doctor capacity.

        Returns:
            dict: Snapshot of the simulation state after the tick.
        """
        self.day += 1

        # --- Reset daily counters ---
        for pharmacy in self.pharmacies:
            pharmacy.reset_daily_count()

        # --- Spread infection and update health for all patients ---
        self._spread_infection()

        # --- Handle hospital admissions ---
        # filter() to find infected patients who need admission
        needs_admission = list(filter(
            lambda p: p.health_status == "Infected"
                      and not p.admitted,
            self.patients
        ))

        for patient in needs_admission:
            self._try_admit_patient(patient)

        # --- Treat admitted infected patients ---
        self._treat_patients()

        # --- Handle discharges ---
        # filter() to find patients who can be discharged
        can_discharge = list(filter(
            lambda p: p.admitted and p.health_status in ("Healthy", "Deceased"),
            self.patients
        ))

        for patient in can_discharge:
            self._discharge_patient(patient)

        return self.get_state()

    def _spread_infection(self) -> None:
        """
        Spread infection across the population and update everyone's health.

        Infects a flat percentage of healthy patients based on the active
        mode's infection rate (higher in pandemic mode), then advances every
        patient's health state. Records the daily and cumulative infection
        and death counts.
        """
        self.daily_new_infections = 0
        self.daily_new_deaths = 0

        # filter() to find susceptible (healthy) patients
        susceptible = list(filter(
            lambda p: p.health_status == "Healthy",
            self.patients
        ))

        # Population-level infection: infect a percentage of healthy patients
        num_to_infect = round(len(susceptible) * self.mode.infection_rate)
        if num_to_infect > 0 and susceptible:
            to_infect = random.sample(
                susceptible, min(num_to_infect, len(susceptible))
            )
            for patient in to_infect:
                # Recovered patients carry acquired immunity and usually
                # resist reinfection
                if patient.resists_infection():
                    continue
                patient.infect()
                self.daily_new_infections += 1
                self.total_infections += 1

        # map() to apply health updates to all patients
        previous_statuses = {p.id: p.health_status for p in self.patients}
        list(map(
            lambda p: p.update_health(is_pandemic=self.mode.is_pandemic),
            self.patients
        ))

        # Count deaths by checking the status changes
        for patient in self.patients:
            prev = previous_statuses.get(patient.id)
            if prev != "Deceased" and patient.health_status == "Deceased":
                self.daily_new_deaths += 1
                self.total_deaths += 1

    def _try_admit_patient(self, patient: Patient) -> bool:
        """
        Try to admit a patient to a hospital with available capacity.

        Returns:
            bool: True if successfully admitted.
        """
        # List comprehension to find hospitals with available beds
        available_hospitals = [
            h for h in self.hospitals if h.available_beds > 0
        ]

        if available_hospitals:
            hospital = available_hospitals[0]
            # List comprehension to filter available doctors at this hospital
            hospital_doctors = [
                d for d in self.doctors
                if d.assigned_facility == hospital.id
                and len(d.assigned_patients) < d.max_patients
            ]

            if hospital_doctors:
                doctor = hospital_doctors[0]
                if hospital.admit_patient(patient.id):
                    patient.admit(hospital.id, doctor.id)
                    doctor.assign_patient(patient.id)
                    return True
        return False

    def _discharge_patient(self, patient: Patient) -> None:
        """Discharge a patient from their assigned hospital."""
        hospital = self._find_hospital(patient.assigned_facility)
        hospital.discharge_patient(patient.id)

        doctor = self._find_doctor(patient.assigned_doctor)
        doctor.remove_patient(patient.id)
        
        patient.discharge()

    def _treat_patients(self) -> None:
        """
        Treat all admitted infected patients.

        Each treatment: doctor's assigned patient gets 1 medicine from
        pharmacy, immunity +0.05. After up to 4 treatments, patient
        becomes Healthy (immunity > 0.50) or Deceased.

        Uses filter() to find patients needing treatment.
        """
        # filter() to find admitted infected patients
        admitted_infected = list(filter(
            lambda p: p.admitted and p.health_status == "Infected",
            self.patients
        ))

        for patient in admitted_infected:
            # Dispense 1 medication from a pharmacy
            self._dispense_medication_for_patient(patient)
            # Apply treatment (immunity boost + threshold check)
            patient.treat()

    def _dispense_medication_for_patient(self, patient: Patient) -> None:
        """Dispense one medication from a pharmacy for a patient's treatment."""
        if self.pharmacies:
            med_name = random.choice(MEDICATIONS)
            pharmacy = random.choice(self.pharmacies)
            pharmacy.fill_prescription(med_name)

    def _find_hospital(self, hospital_id: str | None) -> Hospital | None:
        """Find a hospital by ID."""
        if not hospital_id:
            return None
        matches = [h for h in self.hospitals if h.id == hospital_id]
        return matches[0] if matches else None

    def _find_doctor(self, doctor_id: str | None) -> Doctor | None:
        """Find a doctor by ID."""
        if not doctor_id:
            return None
        matches = [d for d in self.doctors if d.id == doctor_id]
        return matches[0] if matches else None

    def _get_health_updates(self) -> dict:
        """
        Count patients in each health compartment.

        Returns:
            dict: Counts for healthy, infected, deceased, and total.
        """
        healthy = len([p for p in self.patients if p.health_status == "Healthy"])
        infected = len([p for p in self.patients if p.health_status == "Infected"])
        deceased = len([p for p in self.patients if p.health_status == "Deceased"])

        return {
            "healthy": healthy,
            "infected": infected,
            "deceased": deceased,
            "total": len(self.patients),
        }

    def _get_pandemic_stats(self) -> dict:
        """
        Build the pandemic statistics block for API responses.

        Returns:
            dict: Cumulative and daily infection and death counts.
        """
        return {
            "total_infections": self.total_infections,
            "total_deaths": self.total_deaths,
            "daily_new_infections": self.daily_new_infections,
            "daily_new_deaths": self.daily_new_deaths,
        }

    def set_mode(self, mode: str) -> dict:
        """
        Switch the simulation mode and apply its surge capacity.

        Pandemic mode scales up hospital bed capacity and each doctor's
        patient load via the surge multiplier. Normal mode restores base
        capacity and clears the pandemic infection counters.

        Args:
            mode: 'normal' or 'pandemic'.

        Returns:
            dict: Updated mode configuration.
        """
        self.mode.set_mode(mode)

        # Apply surge capacity to hospitals and doctors for the new mode
        multiplier = self.mode.surge_capacity_multiplier
        for hospital in self.hospitals:
            hospital.apply_surge_capacity(multiplier)
        for doctor in self.doctors:
            doctor.apply_surge_capacity(multiplier)

        # Returning to normal clears the pandemic infection counters
        if mode == "normal":
            self.total_infections = 0
            self.total_deaths = 0
            self.daily_new_infections = 0
            self.daily_new_deaths = 0

        return self.mode.to_dict()

    def get_state(self) -> dict:
        """
        Get a complete snapshot of the simulation state.
        Uses map() to serialize all objects.

        Returns:
            dict: Full simulation state for the API.
        """
        # map() to convert all patients to dicts
        patients_data = list(map(lambda p: p.to_dict(), self.patients))
        # map() to convert all doctors to dicts
        doctors_data = list(map(lambda d: d.to_dict(), self.doctors))
        # map() to convert all hospitals to dicts
        hospitals_data = list(map(lambda h: h.to_dict(), self.hospitals))
        # map() to convert pharmacies to dicts
        pharmacies_data = list(map(lambda p: p.to_dict(), self.pharmacies))

        # --- Aggregate stats using reduce() ---
        total_occupied = reduce(
            lambda acc, h: acc + h.occupied_beds,
            self.hospitals, 0
        )
        total_capacity = reduce(
            lambda acc, h: acc + h.total_beds,
            self.hospitals, 0
        )
        # reduce() to count total medicines across all pharmacies
        total_medicines = reduce(
            lambda acc, ph: acc + sum(ph.inventory.values()),
            self.pharmacies, 0
        )

        return {
            "day": self.day,
            "mode": self.mode.to_dict(),
            "overview": {
                "total_patients": len(self.patients),
                "total_doctors": len(self.doctors),
                "total_hospitals": len(self.hospitals),
                "total_pharmacies": len(self.pharmacies),
                "total_beds": total_capacity,
                "total_occupied_beds": total_occupied,
                "total_available_beds": total_capacity - total_occupied,
                "overall_occupancy": round(
                    (total_occupied / total_capacity * 100), 1
                ) if total_capacity > 0 else 0,
                "total_medicines_left": total_medicines,
            },
            "patients": patients_data,
            "doctors": doctors_data,
            "hospitals": hospitals_data,
            "pharmacies": pharmacies_data,
            "pandemic": self._get_pandemic_stats() if self.mode.is_pandemic else None,
            "sir": self._get_health_updates() if self.mode.is_pandemic else None,
        }

    def reset(self) -> None:
        """
        Reset the simulation to Day 0 with fresh population and facilities.
        Re-initializes everything from scratch.
        """
        self.__init__(num_patients=self.num_patients)
