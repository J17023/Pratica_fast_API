from pymongo import MongoClient
from  pymongo.server_api import ServerApi

uri = "mongodb+srv://python:python@cluster0.8cm0d.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

database = MongoClient(uri,server_api= ServerApi('1') ).python

try:
    database.admin.command('ping')
    print('Pinged your deployment. You successfully connected to MongoDB!')
except Exception as e:
    print(str(e))