#Firstly, edit the inventory.json files with the access parameters to the data sources
#Secondly, to get the NFS Server running
ansible-playbook nfs_servers.yaml -i inventory.json

#To run Cassandra on all the servers and to start the script for adding data to the data catalog
ansible-playbook cassandradeploy.yaml -i inventory.json

