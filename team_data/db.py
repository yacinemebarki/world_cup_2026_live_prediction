import sqlite3
import pandas as pd



con=sqlite3.connect("match.db")
cursor=con.cursor()

cursor.execute("DROP TABLE IF EXISTS matches")
con.commit()

class features:
    def __init__(self,date,home_team,away_team,home_team_goals,away_team_goals,home_team_age,away_team_age,home_rank,home_points,home_rank_change,home_previous_points,home_conf,away_rank,away_points,away_rank_change,away_previous_points,away_conf):
        self.home_team=home_team
        self.away_team=away_team
        self.home_team_goals=home_team_goals
        self.away_team_goals=away_team_goals
        self.home_team_age=home_team_age
        self.away_team_age=away_team_age
        self.home_rank=home_rank
        self.home_points=home_points
        self.home_previous_points=home_previous_points
        self.home_rank_change=home_rank_change
        self.home_conf=home_conf
        self.away_rank=away_rank
        self.away_points=away_points
        self.away_rank_change=away_rank_change
        self.away_previous_points=away_previous_points
        self.away_conf=away_conf
        self.date=date  


cursor.execute("""
CREATE TABLE matches(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    home_team TEXT,
    away_team TEXT,
    home_team_goals INTEGER,
    away_team_goals INTEGER,
    home_team_age REAL,
    away_team_age REAL,
    date TEXT,
    home_rank INTEGER,
    home_points INTGER,
    home_rank_change INTGER,
    home_previous_points INTEGER,
    home_conf TEXT,
    away_rank INTGER,
    away_points INTEGER,
    away_rank_change INTEGER,
    away_previous_points INTGER,
    away_conf TEXT)           """)
con.commit()



def insert(match):
    cursor.execute("""
        INSERT INTO matches (
            home_team, away_team,
            home_team_goals, away_team_goals,
            home_team_age, away_team_age,
            date,
            home_rank, home_points, home_rank_change, home_previous_points, home_conf,
            away_rank, away_points, away_rank_change, away_previous_points, away_conf
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        match.home_team,
        match.away_team,
        match.home_team_goals,
        match.away_team_goals,
        match.home_team_age,
        match.away_team_age,
        match.date,
        match.home_rank,
        match.home_points,
        match.home_rank_change,
        match.home_previous_points,
        match.home_conf,
        match.away_rank,
        match.away_points,
        match.away_rank_change,
        match.away_previous_points,
        match.away_conf
    ))

    con.commit()

df=pd.read_csv("team_data/matches.csv")

for i in range(len(df)):
    row=df.iloc[i]
    obj=features(
        date=row["date"],
        home_team=row["home_team"],
        away_team=row["away_team"],

        home_team_goals=row["home_team_goals"],
        away_team_goals=row["away_team_goals"],
        
        home_team_age=row["home_team_age"],
        away_team_age=row["away_team_age"],

        home_rank=row["home_rank"],
        home_points=row["home_total_points"],
        home_rank_change=row["home_rank_change"],
        home_previous_points=row["home_previous_points"],
        home_conf=row["home_conf"],

        away_rank=row["away_rank"],
        away_points=row["away_total_points"],
        away_rank_change=row["away_rank_change"],
        away_previous_points=row["away_previous_points"],
        away_conf=row["away_conf"]
    )
    insert(obj)


    
