from fastapi import FastAPI, Header, HTTPException
from pymongo import MongoClient, ASCENDING
import os

app = FastAPI(title="HPCL Lead Ingestion API")

# ENV VARIABLES (SET THESE IN RENDER)
MONGO_URI = os.environ["MONGODB_URI"]
API_KEY = os.environ["INGEST_API_KEY"]

client = MongoClient(
    MONGO_URI,
    maxPoolSize=50,
    minPoolSize=5,
    serverSelectionTimeoutMS=5000
)

db = client.get_default_database()
collection = db["qualified_leads"]

collection.create_index(
    [("lead_id", ASCENDING)],
    unique=True
)

@app.get("/")
def health():
    return {"status": "HPCL Lead API Running 🚀"}

def verify_api_key(x_api_key: str):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/ingest-leads")
def ingest_leads(leads: list, x_api_key: str = Header(None)):

    verify_api_key(x_api_key)

    upserted = 0
    modified = 0

    for lead in leads:

        if "lead_id" not in lead:
            continue

        result = collection.update_one(
            {"lead_id": lead["lead_id"]},
            {"$set": lead},
            upsert=True
        )

        if result.upserted_id:
            upserted += 1
        elif result.modified_count:
            modified += 1

    return {
        "status": "success",
        "upserted": upserted,
        "modified": modified
    }
