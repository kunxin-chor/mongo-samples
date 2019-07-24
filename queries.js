//NOTE: The following only works when copied and pasted into mongo shell.
db.listingsAndReviews.find({}).limit(5).pretty()

// find all the listings that have 5 beds
db.listingsAndReviews.find({
    'beds':5
}).limit(5).pretty();

// find all the listings that have more than 2 beds
db.listingsAndReviews.find({
    beds:{
        $gt:2
    }
}).limit(5).pretty()

// projecting to only 2 fields -- the address and the beds
db.listingsAndReviews.find({
    beds:{
        $gt:2
    }
}, {address:1, beds:1}).limit(5).pretty()

// find listings that are in Canada (nested syntax)
db.listingsAndReviews.find({
    'address.country':'Canada'
}, {address:1}).limit(5).pretty()

// count the number of listings that are in Canada
db.listingsAndReviews.find({
    'address.country':'Canada'
}).count()

// Find all listings that have more than 2 beds and less than 6 beds (ie, 3 to 5 beds)
db.listingsAndReviews.find({
    beds:{
        $gt:2,
        $lt:6
    }
}, {address:1, beds:1}).limit(5).pretty()

// Find all listings that have more than 2 beds and less than 6 beds (ie, 3 to 5 beds)
db.listingsAndReviews.find({
    $and:[
      {
          beds: {
              $gte:2,
              $lte:6
          }
      },
      {
          'address.country': 'Canada'
      }
   ]
}, {address:1, beds:1}).limit(5).pretty()

/*
SELECT address, beds FROM listingsAndReviews WHERE beds >= 2 AND beds <=6 AND country = 'Canada'
*/

db.listingsAndReviews.find({
    $or:[
        {
            $and:[
                {
                    'address.country':'Canada'
                },
                {
                    beds: {
                        $gte:3,
                        $lte:6
                    }
                }
            ]
        },
        {
            $and:[
                {
                    'address.country':'Portugal'
                },
                {
                    beds: {
                        $gte:7
                    }
                }
            ]
        }
    ]
}, {address:1, beds:1}).sort({'address.country':-1}).limit(10).pretty()

/*
SELECT address, beds FROM listingsAndReviews WHERE (country = 'Canada' AND beds >= 3 AND beds <=6) OR
(country = 'Portugal' AND beds >=10)
*/

// Find only listings with watefront as part of amenities
db.listingsAndReviews.find({
    amenities:"Waterfront"
}, {address:1, amenities:1}).limit(5).pretty()

// Find listings which amenities include waterfront AND coffee maker
db.listingsAndReviews.find({
    amenities: { $all : ['Waterfront', 'Coffee maker'] }
}, {address:1, amenities:1}).limit(5).pretty()

// Find listings which amenities incliude waterfront OR coffee maker
db.listingsAndReviews.find({
    amenities: { $or : ['Waterfront', 'Coffee maker'] }
}, {address:1, amenities:1}).limit(5).pretty()

// All this below are for the sample_mflix database
db.movies.count()

// Find all movies released before 2000
db.movies.find({
    year: {
        $lt:2000
    }
}).count();

db.movies.find({
    countries: "USA"
}).limit(10).pretty()

db.movies.find({
    countries: {
        $nin:['USA']
    }
}, {title:1, countries:1}).limit(10).pretty()

db.movies.find({
    'awards.wins': {
        $gte:3
    }
})

db.movies.find({
    cast:'Tom Cruise'
})

// Find movies that cast Tom Cruise OR Cameron Diaz
db.movies.find({
    cast: {
        $in: ['Tom Cruise', 'Cameron Diaz']
    }
}).pretty().find()

// Find movies that cast Tom Cruise AND Cameron Diaz
db.movies.find({
    cast: {
        $all: ['Tom Cruise', 'Cameron Diaz']
    }
}, {title:1, cast:1}).pretty()

db.movies.find({
    directors: 'Charles Chaplin'
}).count()

// Must pay money in MongoDB for this to work
db.movies.find({
    $where: 'this.directors.length > 1'
}, {title:1, directors:1}).pretty();


db.movies.find({
    'directors.1' : {
        $exists: true
    }
}).count()

// find all theatres in the state of AZ
db.theatres.find({
    'location.address.state':'AZ'
}).count()

//// THIS IS FOR THE TODO APP
db.tasks.insert({
    title: "Walk the dog",
    completed:false
})


// INSERT MANY TODOS
db.tasks.insertMany([
    { title: "Pay the bill", completed:false },
    { title: "Wash the clothes", completed: false },
    { title: "Pay income tax", completed: false }
        
])

// TODO FORMAT
db.tasks.insert({
    title: 'Pick up parcel from PostOffice',
    description: 'It is at the Tiong Bahru Post Office',
    completed: false,
    started: false
})


db.tasks.find({}).pretty()