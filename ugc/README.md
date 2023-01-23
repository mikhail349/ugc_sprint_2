# API-сервис по работе с UGC

## Документация API (Swagger)

1. API доступно по api `/api/v1/openapi`

## Первый запуск

1. Создать файл `.env` с переменными окружения по аналогии с файлом `.env.example`
2. Запустить докер `docker compose up -d --build`
3. Настроить кластер MongoDB
```
docker-compose exec configsvr01 sh -c "mongosh < /scripts/init-configserver.js"
docker-compose exec shard01-a sh -c "mongosh < /scripts/init-shard01.js"
docker-compose exec shard02-a sh -c "mongosh < /scripts/init-shard02.js"
docker-compose exec router01 sh -c "mongosh < /scripts/init-router.js"
docker-compose exec router01 sh -c "mongosh < /scripts/enable-sharding.js"
```
4. Настроить кластер ClickHouse

Подключиться к `docker exec -it clickhouse-node1 sh -c "clickhouse-client"` и выполнить команды:
```
CREATE DATABASE shard;
CREATE DATABASE replica;

CREATE TABLE shard.views (id String, user_id String, movie_id String, timestamp Int64) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/views', 'replica_1') PARTITION BY user_id ORDER BY id;
CREATE TABLE replica.views (id String, user_id String, movie_id String, timestamp Int64) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/views', 'replica_2') PARTITION BY user_id ORDER BY id;
CREATE TABLE default.views (id String, user_id String, movie_id String, timestamp Int64) ENGINE = Distributed('company_cluster', '', views, rand());

exit
```

Подключиться к `docker exec -it clickhouse-node3 sh -c "clickhouse-client"` и выполнить команды:
```
CREATE DATABASE shard;
CREATE DATABASE replica;

CREATE TABLE shard.views (id String, user_id String, movie_id String, timestamp Int64) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/views', 'replica_1') PARTITION BY user_id ORDER BY id;
CREATE TABLE replica.views (id String, user_id String, movie_id String, timestamp Int64) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/views', 'replica_2') PARTITION BY user_id ORDER BY id;
CREATE TABLE default.views (id String, user_id String, movie_id String, timestamp Int64) ENGINE = Distributed('company_cluster', '', views, rand());

exit
```

## Линтер

Запуск: `flake8 src/`