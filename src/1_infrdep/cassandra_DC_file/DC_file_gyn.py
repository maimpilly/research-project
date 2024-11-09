#!/usr/bin/env python3

import json
import yaml

with open("./IAS_Project/infrdep/inventory.json", "r") as inventory:
    hosts_inventory = json.load(inventory)
    
nodes_list = hosts_inventory["all"]["children"]["activ_nodes"]["hosts"]



str=f"CASSANDRA_SEEDS=" 



for node in nodes_list:
    ip_add = nodes_list[node]["ansible_host"]
    str = f"{str}{ip_add}, "

str = str[:-2]

for node in nodes_list:
    with open("./IAS_Project/infrdep/cassandra_DC_file/docker_compose_template.json", "r") as template:
        dc_dict= json.load(template)
    
    with open("./IAS_Project/infrdep/cassandra_DC_file/server_info_template.json", "r") as server_info_temp:
        ser_info = json.load(server_info_temp)

    ser_info["server_name"] = node
    ser_info["server_ip"] = nodes_list[node]["ansible_host"]
    ser_info["user"] = nodes_list[node]["ansible_user"]
    ser_info["psw"] = nodes_list[node]["ansible_ssh_pass"]
    ser_info_file = f"./IAS_Project/infrdep/cassandra_DC_file/{node}.json"  

    ip_add = nodes_list[node]["ansible_host"]
    str2=f"CASSANDRA_BROADCAST_ADDRESS={ip_add}"
    dc_dict["services"]["catalogue_distribution"]["environment"].insert(0,str)
    dc_dict["services"]["catalogue_distribution"]["environment"].insert(1,str2)
    dc_file = f"./IAS_Project/infrdep/cassandra_DC_file/{node}.yaml"  
    
    with open(ser_info_file, "w+") as server:
        json.dump(ser_info,server, sort_keys=False)


    with open(dc_file, "w+") as DC_file:
        yaml.dump(dc_dict, DC_file,sort_keys=False)



print(dc_dict)
