### docker - postgresql
## Link => https://towardsdatascience.com/how-to-run-postgresql-using-docker-15bf87b452d4
docker-compose up

@@ Connect to psql
docker exec -it vehicle_management_postgres_db_1 bash
psql --host=vehicle_management_postgres_db_1 --dbname=vehicle_management --username=lifestyle
psql -h vehicle_management_postgres_db_1 -d vehicle_management -U lifestyle

@@ Load data from a file
psql -h pg_container -d test_db -U root -f infile

----------------------------------------------------------------


# 1. Login to docker
$ sudo docker login

# 2. docker build -t <hub-user>/<repo-name>[:<tag>]
$ sudo docker build -t natthapol593/people-counting:v0.1.0 .

# 3. docker tag <existing-image> <hub-user>/<repo-name>[:<tag>]
$ sudo docker tag -t natthapol593/people-counting:v0.1.0

# 4. docker commit <existing-container> <hub-user>/<repo-name>[:<tag>]

# 5. Push image
# docker push <hub-user>/<repo-name>:<tag>
$ sudo docker push natthapol593/people-counting:v0.1.0


# 6. Pull Image
$ docker pull natthapol593/people-counting:v0.1.0

# 7. Deploy
docker run -it -d --rm --name people-counting -p 5000:5000 natthapol593/people-counting:v0.1.0
docker run -it -d --name people-counting -p 5000:5000 natthapol593/people-counting:v0.1.0

# test deploy
docker run -it --rm --name people-counting -p 5000:5000 natthapol593/people-counting:v0.1.0


# ----------------------------------
@ Redis part 1: with Docker
https://prosbeginner.medium.com/%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B9%83%E0%B8%AB%E0%B8%A1%E0%B9%88-redis-part-1-with-docker-a3a4bfcfd604



