from fastapi import FastAPI, Header, HTTPException
from pymongo import MongoClient, ASCENDING
import os

# =====================================================
# 🚀 FASTAPI INIT
# =====================================================

app = FastAPI(title="HPCL Lead Ingestion API")


# =====================================================
# 🔐 ENV VARIABLES
# =====================================================

MONGO_URI = os.environ["MONGODB_URI"]
API_KEY = os.environ["INGEST_API_KEY"]


# =====================================================
# 🔥 MONGO CONNECTION (PRODUCTION SETTINGS)
# =====================================================

client = MongoClient(
    MONGO_URI,
    maxPoolSize=50,
    minPoolSize=5,
    serverSelectionTimeoutMS=5000
)

db = client.get_default_database()
collection = db["qualified_leads"]


# =====================================================
# ⭐ PREVENT DUPLICATE LEADS (VERY IMPORTANT)
# =====================================================

# Creates index only once
collection.create_index(
    [("lead_id", ASCENDING)],
    unique=True
)


# =====================================================
# ❤️ HEALTH CHECK (Render uses this)
# =====================================================

@app.get("/")
def health():
    return {"status": "HPCL Lead API Running 🚀"}


@app.get("/health")
def health_check():
    try:
        client.admin.command("ping")
        return {"mongo": "connected"}
    except:
        raise HTTPException(status_code=500, detail="Mongo not reachable")


# =====================================================
# 🔐 AUTH HELPER
# =====================================================

def verify_api_key(x_api_key: str):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


# =====================================================
# 🚀 INGEST ENDPOINT
# =====================================================

@app.post("/ingest-leads")
def ingest_leads(leads: list, x_api_key: str = Header(None)):

    verify_api_key(x_api_key)

    if not leads:
        raise HTTPException(status_code=400, detail="No leads provided")

    upserted = 0
    modified = 0

    for lead in leads:

        # Basic validation
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
