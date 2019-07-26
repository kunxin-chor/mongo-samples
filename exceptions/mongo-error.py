import pymongo
import os

db_uri = "mongodb+srv://{}:{}@cluster0-0exhq.mongodb.net/test?retryWrites=true&w=majority"
db_name = 'sample_airbnb'
conn = None
while True:
    try:
        username = input('Please enter your user name: ')
        password = input("Please enter your password: ")
        db_string = db_uri.format(username, password)
        conn = pymongo.MongoClient(db_string)
        conn[db_name]["listingsAndReviews"].find_one({})
        break
    except pymongo.errors.OperationFailure:
        print("Sorry we cannot access the database at the moment...")
        print("Please check your login")
    except pymongo.errors.ConnectionFailure:
        print("The database cannot be reached")
    except Exception as e:
        print("General failure. Please try again later")
    finally:
        print("*----*")
print("Database connected!")
    
doc = conn[db_name]["listingsAndReviews"].find({
    'address.country':'Canada'
}).limit(10)

for d in doc:
    print("Name:", d['name'])
    print("Price: $", d['price'])
    print('-------')



if conn is not None:
    conn.close()