from fastapi import FastAPI
from pymongo import MongoClient
import os

app = FastAPI()

MONGO_URI = os.environ["MONGODB_URI"]
client = MongoClient(MONGO_URI)
db = client.get_default_database()
collection = db["qualified_leads"]


@app.get("/")
def home():
    return {"status": "HPCL Lead API running"}


@app.post("/ingest-leads")
def ingest_leads(leads: list):
    upserted = 0
    modified = 0

    for lead in leads:
        result = collection.update_one(
            {"lead_id": lead["lead_id"]},
            {"$set": lead},
            upsert=True,
        )

        if result.upserted_id:
            upserted += 1
        elif result.modified_count:
            modified += 1

    return {
        "message": "Leads processed successfully",
        "upserted": upserted,
        "modified": modified
    }
