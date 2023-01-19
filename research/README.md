# Исследование по выбору хранилища оценок и избранных фильмов

## Запуск
1. Сформировать виртуальное Python-окружение `python -m venv venv`
2. Установить зависимости `pip install -r requirements.txt`
3. Создать файл `.env` с переменными окружения по аналогии с файлом `.env.example`
4. Запустить докер `docker compose up -d`
5. Настроить кластер MongoDB
```
docker-compose exec configsvr01 sh -c "mongosh < /scripts/init-configserver.js"
docker-compose exec shard01-a sh -c "mongosh < /scripts/init-shard01.js"
docker-compose exec shard02-a sh -c "mongosh < /scripts/init-shard02.js"
docker-compose exec router01 sh -c "mongosh < /scripts/init-router.js"
```
Подключиться к маршрутизатору
```
docker-compose exec router01 mongosh --port 27017
```
и выполнить в консоли
```
sh.enableSharding("movies")
db.adminCommand( { shardCollection: "movies.fav_movies", key: { user_id: "hashed" } } )
db.adminCommand( { shardCollection: "movies.movies_score", key: { movie_id: "hashed" } } )
exit()
```
6. Настроить кластер ClickHouse

Подключиться к
```
docker exec -it clickhouse-node1 sh -c "clickhouse-client"
```
и выполнить в консоли
```
CREATE DATABASE shard;
CREATE DATABASE replica;

CREATE TABLE shard.fav_movies (id String, user_id String, movie_id String) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/fav_movies', 'replica_1') PARTITION BY user_id ORDER BY id;
CREATE TABLE replica.fav_movies (id String, user_id String, movie_id String) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/fav_movies', 'replica_2') PARTITION BY user_id ORDER BY id;
CREATE TABLE default.fav_movies (id String, user_id String, movie_id String) ENGINE = Distributed('company_cluster', '', fav_movies, rand());

CREATE TABLE shard.movies_score (id String, user_id String, movie_id String, score UInt8) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/movies_score', 'replica_1') PARTITION BY movie_id ORDER BY id;
CREATE TABLE replica.movies_score (id String, user_id String, movie_id String, score UInt8) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/movies_score', 'replica_2') PARTITION BY movie_id ORDER BY id;
CREATE TABLE default.movies_score (id String, user_id String, movie_id String, score UInt8) ENGINE = Distributed('company_cluster', '', movies_score, rand());
exit
exit
```

Подключиться к
```
docker exec -it clickhouse-node3 sh -c "clickhouse-client"
```
и выполнить в консоли
```
CREATE DATABASE shard;
CREATE DATABASE replica;

CREATE TABLE shard.fav_movies (id String, user_id String, movie_id String) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/fav_movies', 'replica_1') PARTITION BY user_id ORDER BY id;
CREATE TABLE replica.fav_movies (id String, user_id String, movie_id String) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/fav_movies', 'replica_2') PARTITION BY user_id ORDER BY id;
CREATE TABLE default.fav_movies (id String, user_id String, movie_id String) ENGINE = Distributed('company_cluster', '', fav_movies, rand());

CREATE TABLE shard.movies_score (id String, user_id String, movie_id String, score UInt8) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/movies_score', 'replica_1') PARTITION BY movie_id ORDER BY id;
CREATE TABLE replica.movies_score (id String, user_id String, movie_id String, score UInt8) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/movies_score', 'replica_2') PARTITION BY movie_id ORDER BY id;
CREATE TABLE default.movies_score (id String, user_id String, movie_id String, score UInt8) ENGINE = Distributed('company_cluster', '', movies_score, rand());
exit
exit
```
7. Запустить замер хранилищ `python src/main.py`

## Результаты исследования

- Единица измерения - секунда
- Все операции чтения и записи проводились по 20 раз. В качестве результата взято среднее значение
- В качестве данных использовалось: 200 000 избранных фильмов, 200 000 оценок фильмов

|Операция / Хранилище|MongoDB|Clickhouse|
|-|---------|------------|
|Добавление фильма в избранное|0.004608549995464273|0.01889279999595601|
|Добавление оценки фильму|0.0043648549995850775|0.020752095006173477|
|Чтение избранных фильмов пользователя|0.003956439995090477|0.036465645005227997|
|Чтение оценки фильма|0.00163857500301674|0.029653590003727005|
|Чтение оценки фильма во время записи|0.11965890499996021|0.12154128000547644|

## Итог

Было принято решение доработать действующий сервис, чтобы использовать единую шину доставки сообщений для всех событий - `Kafka`. Такой подход позволит подключать новых слушателей извне, не меняя код API сервиса.

При этом, в качестве хранилища для оценок, рецензий и избранных фильмов принято решение использовать `MongoDB`, т.к. `Clickhouse` предназначен для аналитической работы с большими объемами данных - хуже скорость записи единичных событий и чтения небольшого набора данных по конкретным `id`.