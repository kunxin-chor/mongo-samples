import pymongo
import os

# 1. Retrieve the environment variables
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = 'sample_airbnb'

# 2. Create the connection
conn = pymongo.MongoClient(MONGO_URI)

country = input("Please enter a country: ")

# 3. Query
doc = conn[DATABASE_NAME]["listingsAndReviews"].find({
    'address.country':country
}).limit(10)

for d in doc:
    print("Name:", d['name'])
    print("Price: $", d['price'])
    print('-------')
