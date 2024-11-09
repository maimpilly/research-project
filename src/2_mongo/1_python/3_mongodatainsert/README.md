#To build the python code in a container
docker build -t mongodatainsert .

#Run the container
docker run --network ias_project_default mongodatainsert

#For debugging: Find the container IP of the running mongodb, for changing in the mongo_config.json file
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mongodb


#After running the container:
#To access the container
docker exec -it mongodb mongosh -u admin -p password


Inside-->
#To show databases available:
show dbs;

use ias; #for accessing IAS DB

#To show the collections within ias database
show collections; 

#To show all the data present in the mongodb
db.ias_overview.find()

