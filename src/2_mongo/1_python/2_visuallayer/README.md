#To build the python code in a container
docker build -t visuallayer .

#Run the container
docker run -v /home/researchproject/IAS_Project/mongo/1_python/2_visuallayer/get_module:/usr/src/get_module -v /home/researchproject/IAS_Project/mongo/1_python/2_visuallayer/app:/usr/src/app visuallayer

#For debugging: Find the container IP of the running mongodb, for changing in the mongo_config.json file
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' visuallayer


