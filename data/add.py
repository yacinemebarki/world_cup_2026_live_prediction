import os
import shutil
import re

downlaod_path=os.path.expanduser("~/Downloads")
target_path=os.path.expanduser("~/world_cup_2026_live_prediction/data/additional")

pattern=r"players"
pattern2=r"matches"

for file in os.listdir(downlaod_path):

    if not file.endswith(".csv"):
        continue
    
    match=re.search(pattern, file)
    match2=re.search(pattern2, file)

    if match or match2:
        src_path=os.path.join(downlaod_path, file)
        dest_path=os.path.join(target_path, file)

        
        if os.path.exists(dest_path):
            
            continue
        shutil.move(src_path, dest_path)
                   
                 