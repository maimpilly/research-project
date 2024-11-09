import numpy as np
#from tensorflow.keras.models import load_model
import sys
import os
sys.path.insert(1, "/usr/src/get_module") #for the docker env
from  transfer_files import File_downloader

#dict = {"f_name": "IN ('.csv')"}
dict = {'f_name': "IN ('el_condition=defect_lg=0.75_vgs=None_vds=None.tif','tdr_condition=defect_lg=0p75_vgs=0_vds=None.mat','el_condition=defect_lg=0p25_vgs=-1_vds=4.tif','s11_condition=intact_lg=0p25_vgs=0_vds=4.s1p','tdr_condition=defect_lg=0.75_vgs=None_vds=None.mat')"}
files = File_downloader(dict, "/usr/src/app/data/")
files.ssh_file_transfer()
files.cloud_file_transfer()

print("check the files plz")

# # Load stored model
# model_dir = "best_cnn_model_run_1.h5"
# model_pretrained = load_model(model_dir)

# # Load an exemplary data file
# tdr_data = np.loadtxt("./data/"+os.listdir("./data")  [0], delimiter=',')[:, 2]
# tdr_data_downsampled = tdr_data[0::4]
# tdr_data_analysis = np.reshape(tdr_data_downsampled, [1, len(tdr_data_downsampled), 1])

# class_code = model_pretrained.predict(tdr_data_analysis)
# print(class_code)
