from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime
import re

url="https://www.worldfootball.net/competition/co139/fifa-world-cup/team-statistics-overview/"
base="https://www.worldfootball.net"
path="./team_data"




def cal_age(match_day, birthday):
    
    birthday_clean = re.search(r"\d{2}\.\d{2}\.\d{4}", birthday)
    if not birthday_clean:
        
        return None
    birthday_dt = datetime.strptime(birthday_clean.group(), "%d.%m.%Y")
    
    match_day = datetime.fromisoformat(match_day.replace("Z", "+00:00"))
    age=match_day.year-birthday_dt.year
    
    
    return age

with sync_playwright() as p:
    
    browser=p.chromium.launch(headless=False,args=["--disable-blink-features=AutomationControlled"])
    page=browser.new_page()
    page.goto(url,wait_until="domcontentloaded",timeout=60000)
  
    html=page.content()
    soup=BeautifulSoup(html, "html.parser")
    teams=soup.select("td.team-name")

    for t in teams:
        
        dic=t.text.strip()
        dic=os.path.join(path,dic)
        
        if not os.path.exists(dic):
            os.makedirs(dic)
        
        link=base+t.find("a")["href"]+"all-matches/"
        page.goto(link,wait_until="domcontentloaded",timeout=60000)
        html=page.content()
        team_soup=BeautifulSoup(html,"html.parser")
        option=team_soup.select("select.navigation.season-navigation option")
        valid_years = [opt for opt in option if opt.text.strip().isdigit() and int(opt.text.strip()) >= 1998]
            
        
        for year in valid_years:
            
            year_link=base+year["value"]
            year_nu=year.text.strip()
            
            
            page.goto(year_link,wait_until="domcontentloaded",timeout=60000)
            html=page.content()
            matche_soup=BeautifulSoup(html,"html.parser")
            all_matche=matche_soup.select('tr[data-match_id]')
            matches=[]
            
            for matche in all_matche:
                
                matche_dt=matche.get('data-datetime')
                where=matche.find("td",class_="match-homeaway").text.strip()
                oppo=matche.find("td",class_="team-shortname_extended").text.strip()
                result=matche.select_one("td.match-result span a")
                
                if result.text.strip()!="-:-":
                    
                    oppo_file=oppo+".json"
                    file_path=os.path.join(dic,oppo_file)
                    report_link=base+result["href"]    
                    page.goto(report_link,wait_until="domcontentloaded",timeout=60000)
                    html=page.content()
                    player_soup=BeautifulSoup(html,"html.parser")
                    
                    home_team=player_soup.select_one("div.hs-lineup--starter.home")
                    away_team=player_soup.select_one("div.hs-lineup--starter.away")
                    
                    players_home=home_team.select(".person-name a")
                    players_away=away_team.select(".person-name a")
                    
                    home=0
                    away=0
                    
                    for player in players_home:
                        player_link=base+player["href"]
                        page.goto(player_link,wait_until="domcontentloaded",timeout=60000)
                        html=page.content()
                        info=BeautifulSoup(html,"html.parser")
                        birthday=info.select_one("dd.person-birthday").text
                        age=cal_age(matche_dt,birthday)
                        home=age+home
                        
                    home_age=home/11
                    
                    for player in players_away:
                        player_link=base+player["href"]
                        page.goto(player_link,wait_until="domcontentloaded",timeout=60000)
                        html=page.content()
                        info=BeautifulSoup(html,"html.parser")
                        birthday=info.select_one("dd.person-birthday").text
                        age=cal_age(matche_dt,birthday)
                        away=age+away
                    
                    away_age=away/11
                    
                                           
                        
                        
                        
                    
                    if not os.path.exists(file_path):
                        open(file_path,"a").close()
                        
                        with open(file_path,"w") as f:
                            json.dump({oppo: []},f,indent=4)
                    
                    with open(file_path,"r") as f:
                        data=json.load(f)
                        
                    matches_list=data.get(oppo, [])    
                    n=len(data)
                    new_match={oppo:[{"id":n,"date":matche_dt,"where":where,"result":result.text.strip(),"home_age":home_age,"away_age":away_age}]}
                    matches_list.append(new_match)
                    data[oppo]=matches_list
                    with open(file_path, "w") as f:
                        json.dump(data, f, indent=4)
                    print("matche added")  
                    
                    
                                
                        
                    
    browser.close()






  
        


