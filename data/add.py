import os
import shutil
import re

downlaod_path=os.path.expanduser("~/Downloads")
target_path=os.path.expanduser("~/world_cup_2026_live_prediction/data/additional")

pattern=r"players"
pattern2=r"matches"

for file in os.listdir(downlaod_path):
    if file.endswith(".csv"):
        match=re.search(pattern,file)
        match2=re.search(pattern2,file)
        if match:
            src_path=os.path.join(downlaod_path,file)
            
            shutil.move(src_path,target_path)
        if match2:
            src_path=os.path.join(downlaod_path,file)
            
            shutil.move(src_path,target_path)            
                 