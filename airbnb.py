import pymongo
import os

db_uri = os.getenv('MONGO_URI')
db_name = 'sample_airbnb'

conn = pymongo.MongoClient(db_uri)
db = conn[db_name]

country = input("Please type in a country: ")

# db.listingsAndReviews.find({
#   'address.country' : country   
#}, { name:1, price:1, address: 1 })
listings = db['listingsAndReviews'].find({
    'address.country' : country
}, {'name': 1, 'price':1, 'address': 1})

for l in listings:
    print ("Name: ", l['name'])
    print ("Price: ", l['price'])
    # JS: console.log("Address:", l.address.street)
    print ("Address", l['address']['street'])
    print('-----')
