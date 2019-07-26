from bson.objectid import ObjectId

collection = None
def create_product(product, price, description, quantity):
    if price < 0 or quantity < 0:
        return None
    
    result = collection.insert_one({
        'name': product,
        'price': price,
        'description':description,
        'quantity':quantity
    })
    return result.inserted_id
    
def update_product(taskid, product, price, description, quantity):
    collection.update_one(
        {
            '_id':ObjectId(taskid)
        },
        {
            '$set': {
                '_id':ObjectId(taskid),
                'name': product,
                'price': price,
                'description':description,
                'quantity':quantity
            }
        }
    )