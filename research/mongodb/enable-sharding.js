sh.enableSharding("movies")
db.adminCommand( { shardCollection: "movies.movies_score", key: { movie_id: "hashed" } } )