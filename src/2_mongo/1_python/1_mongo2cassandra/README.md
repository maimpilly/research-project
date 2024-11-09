#To build the python code in a container (Only once)
docker build -t mongo2cassandra .

#Run the container
docker run --network ias_project_default -v /var/run/docker.sock:/var/run/docker.sock mongo2cassandra 

#For debugging: Find the container IP of the running mongodb, for changing in the mongo_config.json file
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' cassandraNode
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mongodb


#After running the container:
#To access the container
docker exec -it cassandraNode cqlsh


Inside container-->
#To show databases available:
describe dbs;

use ias_shares; #for accessing IAS DB

#To show the collections within ias database
show tables; 

#To show all the data present in the mongodb
select * from <tablename>

