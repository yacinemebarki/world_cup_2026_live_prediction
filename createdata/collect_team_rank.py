from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import os 
import csv
import pandas as pd
from datetime import datetime

dates = [
    "18/07/2024",
    "19/09/2024",
    "24/10/2024",
    "28/11/2024",
    "19/12/2024",
    "20/01/2025",
    "03/04/2025",
    "10/07/2025",
    "18/09/2025",
    "17/10/2025",
    "19/11/2025",
    "22/12/2025",
    "19/01/2026",
    "18/03/2026",
    "01/04/2026"
]
for i in range(len(dates)):
    dates[i]=datetime.strptime(dates[i], "%d/%m/%Y").strftime("%Y-%m-%d")

class team:
    def __init__(self,name,rank,point,conf,abrv):
        self.name=name
        self.rank=rank
        self.rank_change=0
        self.prv_point=0
        self.point=point
        self.conf=conf
        self.abrv=abrv
        
        self.conf=None


teams=[]

df=pd.read_csv("./team_data/fifa_ranking-2024-06-20.csv")
df=df[df["rank_date"]=="2024-06-20"]
spcial_teams={"IR Iran":"Iran","Turkey":"Turkiye","Korea Republic":"South Korea","Côte d'Ivoire":"Ivory Coast","Congo DR":"DR Congo","Cabo Verde":"Cape Verde","Curacao":"Curaçao","USA":"United States","Czech Republic":"Czechia"}

for _,row in df.iterrows():
    tea=row["country_full"]
    rank=row["rank"]
    point=row["total_points"]
    conf=row["confederation"]
    abrv=row["country_abrv"]
    if pd.isna(rank):
        rank=None
    else :
        rank=int(rank)    
    if pd.isna(point):
        point=None
    else :
        point=float(point)  
    if tea in spcial_teams:
        tea=spcial_teams[tea]          

    teams.append(team(tea, rank, point, conf,abrv))
   

names=[]
with sync_playwright() as p:
    
    browser=p.chromium.launch(headless=False,args=["--disable-blink-features=AutomationControlled"])
    page=browser.new_page()
    
    for date in dates:
        
        teams_name=[]
        date=date
        for i in range(1,9):
            url=f"https://www.transfermarkt.com/statistik/weltrangliste/statistik/stat/plus/0/galerie/0?page={i}&datum={date}"
            page.goto(url,wait_until="domcontentloaded",timeout=60000)
            html=page.content()
            soup=BeautifulSoup(html,"html.parser")
            

            search_team=soup.select("tr.odd, tr.even")
            
            
            
            
            j=0
            world_cup_teams=teams.copy()
            while(j<len(search_team) and len(world_cup_teams)>0):
                name_tag=search_team[j].select_one("td.hauptlink a")
                
                rank_tag=search_team[j].select_one("td.zentriert.cp")
                
                point_tag=search_team[j].select_one("td.zentriert.hauptlink")
                
                print(name_tag)
                
                
                if not name_tag or not point_tag or not rank_tag:
                    print("somthing not found")
                    
                    j+=1
                    continue

                img=name_tag.select_one("img")
                name=img["alt"]
                
                
                
                

                rank=int(rank_tag.text.strip())
                point=float(point_tag.text.strip())
                print(name,rank,point)
                print(name)
                for te  in world_cup_teams:
                    
                    
                    
                    if te.name==name:
                        if te.rank is not None:
                            te.rank_change = te.rank - rank
                        else:
                            te.rank_change = 0
                        te.rank=rank
                        te.prv_point=te.point
                        te.point=point
                        with open("./team_data/fifa_ranking-2024-06-20.csv","a", newline="") as f:
                            writer=csv.writer(f)
                            writer.writerow([te.rank,te.name,te.abrv,te.point,te.prv_point,te.rank_change,te.conf,date])
                        
                        world_cup_teams.remove(te)
                        print("a teams was add")
                        break
                    

                j+=1    

                
