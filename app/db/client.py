from pymongo import MongoClient

uri = "mongodb://localhost:27017/gestor"

try:
    database = MongoClient(uri)
    db = database["gestor"]
    users = db["user"]
except Exception as e:
    print("Exception " + e)