from pymongo import mongo_client
import pymongo
from app.config import settings

# client = mongo_client.MongoClient(
#     settings.DATABASE_URL, serverSelectionTimeoutMS=5000)

client =mongo_client.MongoClient(
    'mongodb+srv://Gayathri:gayi@cluster0.iosmm7k.mongodb.net/?retryWrites=true&w=majority')
# db = client["registration-db"]
# users = db["users"]
# shipment = db["shipment"]


try:
    conn = client.server_info()
    print(f'Connected to MongoDB {conn.get("version")}')
except Exception:
    print("Unable to connect to the MongoDB server.")

db = client[settings.MONGO_INITDB_DATABASE]
User = db.users
User.create_index([("email", pymongo.ASCENDING)], unique=True)

