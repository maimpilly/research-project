import numpy as np
#from tensorflow.keras.models import load_model
import sys
import os
import glob
sys.path.insert(1, "/usr/src/get_module") #for the docker env
from  transfer_files import File_downloader
import shutil
from pathlib import PurePath

dict = {"f_type":"IN ('.tif', '.jsn', '.bmp', '.s1p', '.mat', '.tiff')"}

files = File_downloader(dict, "/usr/src/app/data/")
files.ssh_file_transfer()
files.cloud_file_transfer()





files_list = glob.glob("/usr/src/app/data/*.*")
#print(files_list)

for url in files_list:
    p = PurePath(url)
    if p.suffix == ".s1p":
        destination = "data/S11_Measurements_on_Pos15_gate/"
        shutil.move(url, destination)
    elif p.suffix == ".mat":
        destination = "data/TDR_Measurements_on_Pos1+5/"
        shutil.move(url, destination)
    elif p.name.split("_")[0] == "Pos1":
        if p.suffix == ".tif":
            destination = "data/EL_Measurements_on_Pos1-5//Pos1/TIFs/"
            shutil.move(url, destination)
        else:
            destination = "data/EL_Measurements_on_Pos1-5//Pos1/"
            shutil.move(url, destination)

    elif p.name.split("_")[0] == "Pos5":
        if p.suffix == ".tif":
            destination = "data/EL_Measurements_on_Pos1-5//Pos5/TIFs/"
            shutil.move(url, destination)
        else:
            destination = "data/EL_Measurements_on_Pos1-5//Pos5/"
            shutil.move(url, destination)

# shutil.rmtree("data")
# shutil.copytree("/usr/src/app/output", "/usr/src/app", symlinks=False, ignore=None, copy_function=copy2, ignore_dangling_symlinks=False, dirt_ok=False)
print("check the files plz")