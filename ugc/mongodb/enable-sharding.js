sh.enableSharding("movies")
db.adminCommand( { shardCollection: "movies.ratings", key: { object_id: "hashed" } } )
db.adminCommand( { shardCollection: "movies.reviews", key: { movie_id: "hashed" } } )