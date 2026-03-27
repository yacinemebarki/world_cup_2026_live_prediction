import os
import shutil
import re

downlaod_path=os.path.expanduser("~/Downloads")
project_path=os.path.expanduser("~/world_cup_2026_live_prediction/data")

pattern=r"world-cup-(\d{4})"

for file in os.listdir(downlaod_path):
    if file.endswith(".csv"):
        match=re.search(pattern,file)
        if match:
            year=match.group(1)
            target_folder=os.path.join(project_path,year)
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
            src_path=os.path.join(downlaod_path,file)
            target_path=os.path.join(target_folder,file)
            shutil.move(src_path,target_path)
                
                