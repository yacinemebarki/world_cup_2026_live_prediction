import csv
import os
import json

path="./team_data"
target_path="./team_data/mathces.csv"

file_exists = os.path.exists(target_path)
csv_file=open(target_path, "a", newline="")
writer=csv.writer(csv_file)

if not file_exists:
    writer.writerow([
        "home_team",
        "away_team",
        "home_team_goals",
        "away_team_goals",
        "home_team_age",
        "away_team_age",
        "date"
    ])

for dirc in os.listdir(path):

    team_path=os.path.join(path,dirc)

    if not os.path.isdir(team_path):
        continue
    
    for file in os.listdir(team_path):
        mathce_path=os.path.join(team_path,file)

        if not os.path.exists(target_path):
            open(target_path,"a").close
            with open(target_path,"w") as f:
                writer=csv.writer(f)
                writer.writerow(["home_team","away_team","home_team_goals","away_team_goals","home_team_age","away_team_age","date"])
        
        oppenet=file.split(".")[0]
        
        with open(mathce_path,"r") as f:
            data=json.load(f)

        matche_list=data.get(oppenet,[])

        for block in matche_list:
            matches=block.get(oppenet,[])
            for matche in matches:
                date=matche["date"]
                where=matche["where"]
                result=matche["result"]
                home_age=matche["home_age"]
                away_age=matche["away_age"]
                if where=="H":
                    home_team=dirc
                    away_team=oppenet
                    home_goals=int(result.split(":")[0])
                    away_goals=int(result.split(":")[1])
                else :
                    away_team=dirc
                    home_team=oppenet
                    home_goals=int(result.split(":")[1])
                    away_goals=int(result.split(":")[0])
                writer.writerow([home_team,away_team,home_goals,away_goals,home_age,away_age,date])    

                



