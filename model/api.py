from fastapi import FastAPI
import pickle
from pydantic import BaseModel
import numpy as np



with open("linear_model.pkl","rb") as f:
    model=pickle.load(f)

with open("team_encoder.pkl","rb") as f:
    team_encoder=pickle.load(f)

with open("conf_encoder.pkl","rb") as f:
    conf_encoder=pickle.load(f)

class InputData(BaseModel):

    home_team: str
    away_team: str

    home_team_age: float
    away_team_age: float

    home_rank: int
    home_points: float
    home_rank_change: int
    home_previous_points: float
    home_conf: str

    away_rank: int
    away_points: float
    away_rank_change: int
    away_previous_points: float
    away_conf: str

           

app=FastAPI()
@app.post('/predict')
async def predict(data :InputData):

    home_team=team_encoder.transform(data.home_team)
    away_team=team_encoder.transform(data.away_team)
    home_conf=team_encoder.transform(data.home_conf)
    away_conf=team_encoder.transform(data.away_conf)
    features = [[
        home_team,
        away_team,
        data.home_team_age,
        data.away_team_age,
        data.home_rank,
        data.home_points,
        data.home_rank_change,
        data.home_previous_points,
        home_conf,
        data.away_rank,
        data.away_points,
        data.away_rank_change,
        data.away_previous_points,
        away_conf
    ]]

    result=model.predict(features)
    result=np.where((result-np.floor(result))>=0.3,np.ceil(result),np.floor(result)).astype(int)
    return {"result":result}
