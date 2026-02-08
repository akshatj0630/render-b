from pymongo import MongoClient

# 🔹 MongoDB connection details
MONGO_URI = "mongodb+srv://akshatjain0630_db_user:Hpcl12345@hpcl.t3mgyrz.mongodb.net/hpcl?retryWrites=true&w=majority"

DB_NAME = "hpcl"
COLLECTION = "qualified_leads"

# 🔹 Create client
client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)

# 🔹 Test connection (optional but recommended)
client.admin.command("ping")

# 🔹 Get DB & Collection
db = client[DB_NAME]
leads_collection = db[COLLECTION]
