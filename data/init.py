import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URL")

client = AsyncIOMotorClient(MONGO_URI)
DB = client[os.getenv("DB_NAME")]

patients_coll = DB[os.getenv("PATIENT_COLLECTION_NAME")]
doctors_coll = DB[os.getenv("DOCTOR_COLLECTION_NAME")]
staff_coll = DB[os.getenv("STAFF_COLLECTION_NAME")]
appointment_coll = DB[os.getenv("APPOINTMENT_COLLECTION_NAME")]
user_coll = DB[os.getenv("USER_COLLECTION_NAME")]