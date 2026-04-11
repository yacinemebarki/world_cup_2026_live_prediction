from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import os 
import csv

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

world_cup_2026_teams = [
    # Hosts
    "Canada", "Mexico", "USA",

    # AFC (Asia)
    "Australia", "IR Iran", "Japan", "Jordan", "Korea Republic",
    "Qatar", "Saudi Arabia", "Uzbekistan",

    # CAF (Africa)
    "Algeria", "Cabo Verde", "Côte d'Ivoire", "Egypt", "Ghana",
    "Morocco", "Senegal", "South Africa", "Tunisia",

    # CONCACAF (North & Central America, Caribbean)
    "Curaçao", "Haiti", "Panama",

    # CONMEBOL (South America)
    "Argentina", "Brazil", "Colombia", "Ecuador", "Paraguay", "Uruguay",

    # OFC (Oceania)
    "New Zealand",

    # UEFA (Europe)
    "Austria", "Belgium", "Bosnia and Herzegovina", "Croatia", "Czech Republic",
    "England", "France", "Germany", "Netherlands", "Norway",
    "Portugal", "Scotland", "Spain", "Sweden", "Switzerland", "Turkey",

    # Play-Off Tournament winners
    "Bolivia", "DR Congo", "Iraq", "Jamaica", "New Caledonia", "Suriname"
]

class team:
    def __init__(self,name):
        self.name=name
        self.rank=0
        self.rank_chaneg=0
        self.prv_point=0
        self.diffpoint=0
        self.conf=0

teams=[]

for tea in world_cup_2026_teams:
    teams.append(team(tea))



with sync_playwright() as p:
    
    browser=p.chromium.launch(headless=False,args=["--disable-blink-features=AutomationControlled"])
    page=browser.new_page()
    
    for date in dates:
        
        teams_name=[]
        date=date
        for i in range(1,5):
            url=f"https://www.transfermarkt.com/statistik/weltrangliste/statistik/stat/plus/0/galerie/0?page={i}&datum={date}"
            page.goto(url,wait_until="domcontentloaded",timeout=60000)
            html=page.content()
            soup=BeautifulSoup(html,"html.parser")
            

            search_team=soup.select("td.hauptlink a")
            
        
            for a in search_team:
                name=a.get_text(strip=True)
                if name:
                    teams_name.append(name)
            print(teams_name)


                   

       


