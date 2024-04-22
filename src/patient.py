"""
TODO: Implement the Patient class.
Please import and use the config and db config variables.

The attributes for this class should be the same as the columns in the PATIENTS_TABLE.

The Object Arguments should only be name , gender and age.
Rest of the attributes should be set within the class.

-> for id use uuid4 to generate a unique id for each patient.
-> for checkin and checkout use the current date and time.

There should be a method to update the patient's room and ward. validation should be used.(config is given)

Validation should be done for all of the variables in config and db_config.

There should be a method to commit that patient to the database using the api_controller.
"""

import uuid
from datetime import datetime
import requests
from config import GENDERS, ROOM_NUMBERS, WARD_NUMBERS, API_CONTROLLER_URL

class Patient:
    def __init__(self, name, gender, age):
        self.patient_id = str(uuid.uuid4())  
        self.patient_name = name
        self.patient_gender = gender
        self.patient_age = age
        self.patient_room = None
        self.patient_ward = None
        self.patient_checkin = datetime.now().isoformat()  
        self.patient_checkout = None
        self.is_new = True  

    def set_room(self, room):
        self.patient_room = room

    def set_ward(self, ward):
        self.patient_ward = ward

    def commit(self):
        if self.patient_room is None or self.patient_ward is None:
            raise ValueError("Both room and ward must be set before committing")

        if self.is_new:
            url = f"{API_CONTROLLER_URL}/patients"
            data = {
                "patient_id": self.patient_id,
                "patient_name": self.patient_name,
                "patient_gender": self.patient_gender,
                "patient_age": self.patient_age,
                "patient_room": self.patient_room,
                "patient_ward": self.patient_ward,
                "patient_checkin": self.patient_checkin,
                "patient_checkout": self.patient_checkout
            }
            response = requests.post(url, json=data)
        else:
            url = f"{API_CONTROLLER_URL}/patient/{self.patient_id}"
            data = {
                "patient_room": self.patient_room,
                "patient_ward": self.patient_ward
            }
            response = requests.put(url, json=data)

        if response.status_code in [200, 201]:
            self.is_new = False  
            return response.json()
        else:
            raise Exception(f"Error committing patient: {response.json().get('error', 'Unknown error')}")

    def get_id(self):
        return self.patient_id

    def get_name(self):
        return self.patient_name

    def get_room(self):
        return self.patient_room

    def get_ward(self):
        return self.patient_ward



