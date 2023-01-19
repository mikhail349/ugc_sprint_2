sh.enableSharding("movies")
db.adminCommand( { shardCollection: "movies.fav_movies", key: { user_id: "hashed" } } )
db.adminCommand( { shardCollection: "movies.movies_score", key: { movie_id: "hashed" } } )