import uuid    #We import this library in order to be able to generate unique ids for all people
import random   #We import this library in order to generate random values within a given range
from typing import List, Optional


class Person:
    def __init__(self, name: str, age: int, gender: str, contact: str):
        self.id: str = uuid.uuid4() [:8]   #Generates a big number, but we take the first 8
        self.name: str =  name
        self.age: int = age
        self.gender: str = gender
        self.contact: str =  contact

#To send the data to our API, we need to transform it into a JSON file
#The to_dict function puts the data in a dictionary format and makes it easier to share the data
    def get_info(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "contact": self.contact,
        }


class Patient(Person):
    #3 Health Statuses
    HEALTH_STATUS = ["Healthy", "Infected", "Deceased"]

    #Treatment Constants
    IMMUNITY_THRESHOLD = 0.50
    MAX_TREATMENTS = 2
    DAYS_UNTIL_DEATH_UNADMITTED = 10

    def __init__(self, name: str, age: int, gender: str, contact: str):
        super().__init__(name, age, gender, contact)
        #it will reuse the attributes of the Person class

        #Attributes specific to the Patient Class
        self.health_status: str = "Healthy" #This means that the patient starts out healthy
        self.immunity: float = round(random.uniform(0.1,0.5), 2)
        self.days_infected: int = 0
        self.treatments_received: int = 0
        #Start at 0 because the patient is not yet infected
        self.admitted: bool = False
        #Boolean value ; the patient is not yet in hospital
        self.assigned_doctor: Optional[str] = None
        self.assigned_facility: Optional[str] = None
        #Patient is not yet sick, so not in hospital and don't have a doctor

    #Functions specific to the Patient Class
    def admit(self, doctor_id: str, facility_id: str) -> None:
        self.admitted = True
        self.assigned_doctor = doctor_id
        self.assigned_facility = facility_id

    def infect(self):
        if self.health_status is not ["Infected", "Deceased"]:
            self.health_status = "Infected"
            #If the patient is not already infected or deceased, then their health status is changed
            self.days_infected = 0
            self.treatments_received = 0
            #the case is handled where patients get healthy after recovering and they discharge from the hospital
            #but they get infected again on the next day

    #Main objective of this function is to return the health status
    def update_health(self) -> str:
        if self.health_status == "Deceased":
            return self.health_status
        if self.health_status == "Infected":
            self.days_infected += 1
            if not self.admitted and self.days_infected > self.DAYS_UNTIL_DEATH_UNADMITTED:
                self.health_status = "Deceased"
        return self.health_status

    def discharge(self):
        self.admitted = False
        self.assigned_doctor = None
        self.assigned_facility = None

        if self.health_status != "Infected":
            return self.health_status
        return None
        #if the health status was healthy then we don't discharge

    def treat(self):
        self.immunity = round((self.immunity+0.1),2)
        self.treatments_received += 1
        if self.immunity >= self.IMMUNITY_THRESHOLD:
            self.health_status = "Healthy"
            self.days_infected = 0
            self.treatments_received = 0
            self.immunity = round(random.uniform(0.1,0.8),2)
        if self.treatments_received >= self.MAX_TREATMENTS:
            self.health_status = "Deceased"
        return self.health_status

    def to_dict(self) -> dict:
        #to be able to convert to json folder for API
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
    def __init__(self, name: str, age: int, gender: str, contact: str):
        super().__init__(name, age, gender, contact)

        #Attributes specific to Doctor class
        self.assigned_patients: List[str] = []
        #stores patient ids in the list
        #couldn't store it as patient_ids because we don't have it in the argument
        self.max_patients: int = 8
        self.assigned_facility: Optional[str] = None
        self.is_available: bool = True

    #Functions specific to Doctor class
    def assign_patient(self,  patient_id:str) -> bool:
        if len(self.assigned_patients) < self.max_patients:
            self.assigned_patients.append(patient_id)
            return True
        return False

    def remove_patient(self, patient_id:str) -> bool:
        if patient_id in self.assigned_patients:
            self.assigned_patients.remove(patient_id)
            return True
        return False

    def to_dict(self) -> dict:
        info = self.get_info()
        info.update({
            "assigned_facility": self.assigned_facility,
            "num_patients": len(self.assigned_patients),
            "max_patients": self.max_patients,
            "available": self.available,
        })
        return info
