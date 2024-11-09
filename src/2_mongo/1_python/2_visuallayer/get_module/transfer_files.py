import boto3
import get_data
import pandas as pd
from paramiko import SSHClient, AutoAddPolicy

# here is the script to transfer the files needed for my ML Algo
# this script will be executed on the main Node (ArchiControll) but can be easaly ajusted and transferd to be executed on any active Node where a microService runs
#-------------------------------------------------------------------files transfert from any NFS shares on the active Nodes------------------------------------------
# Active Nodes are defined in the inventory.json
class File_downloader:
    
    def __init__(self, dict, file_dest):
       self.dict = dict
       self.file_dest = file_dest
       self.worker = get_data.GetData(dict)
       self.files_info = self.worker.catalogue_get()



    def ssh_file_transfer(self):

      #files_info = worker.catalogue_get() # list of files that fullfil the filter creteria

      dup_hosts = [] # set of the host in the files list 
      for file in self.files_info:
        if file.get_methode == "ssh_file_transfer":
          dup_hosts.append({"host":file.host, "username":file.username, "password":file.password})

      hosts = pd.DataFrame(dup_hosts).drop_duplicates().to_dict('records')
    # here the files transfert to the destination 

      ssh = SSHClient()
      ssh.set_missing_host_key_policy(AutoAddPolicy())
      for host in hosts:
          ssh.connect(host["host"], username=host["username"], password=host["password"])
          ftp_client = ssh.open_sftp()
          for file in self.files_info:
              if file.get_methode == "ssh_file_transfer" and file.host == host["host"]:
                  f_destination = f"{self.file_dest}/{file.f_name}"
                  ftp_client.get(file.f_location, f_destination)
          ftp_client.close()

    #------------------------------------------------------files transfert from the cloud: here the example of AWS-S3-Bucket-------------------------------------

    def cloud_file_transfer(self):

      #files_info = worker.catalogue_get() # list of files that fullfil the filter creteria
      for file in self.files_info:
          if file.get_methode == "cloud_file_transfer":
            f_location = file.f_location
            f_credentials = [file.access_key_id, file.access_key]
            self.worker.s3_get(f_location, f_credentials, self.file_dest)
   
    
    


# dict = {"f_type": "IN ('.csv')"}
# files = File_downloader(dict, "/home/yassir/IAS_Project/microservice")
# files.ssh_file_transfer()
# files.cloud_file_transfer()
