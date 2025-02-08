#from typing import Union
import pickle
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

from fastapi import FastAPI
from pydantic import BaseModel
import pickle

from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:4200",  
    "http://127.0.0.1:4200",   
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)



# Load encoders and models
with open("encoder_state.pkl", "rb") as f:
    encoder_state = pickle.load(f)

with open("encoder_area.pkl", "rb") as f:
    encoder_area = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("XGBoost.pkl", "rb") as f:
    model = pickle.load(f)

XGB_importances_column = [
    'Total charge', 'Area code_415', 'Area code_408', 'Customer service calls',
    'Area code_510', 'Total intl calls', 'International plan',
    'Number vmail messages', 'State_SC', 'State_TX', 'State_MT',
    'Total intl charge', 'State_IL', 'CScalls Rate'
]


class PredictionInput(BaseModel):
    State: str
    Total_charge: float
    Area_code: int
    Customer_service_calls: int
    Total_intl_calls: int
    International_plan: int
    Number_vmail_messages: int
    Total_intl_charge: float
    CScalls_Rate: float

@app.post("/predict/")
async def impdata(data: PredictionInput):
    with open("encoder_state.pkl", "rb") as f:
        encoder_state = pickle.load(f)

    with open("encoder_area.pkl", "rb") as f:
        encoder_area = pickle.load(f)

    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)

    with open("XGBoost.pkl", "rb") as f:
        model = pickle.load(f)

    # Encode the state
    encoded_state = encoder_state.transform([[data.State]])[0]
    # Encode the area code
    encoded_area = encoder_area.transform([[data.Area_code]])[0]
    # Combine all data
    features = [
        data.Total_charge, encoded_area[1], encoded_area[0], data.Customer_service_calls,
        encoded_area[2], data.Total_intl_calls, data.International_plan,
        data.Number_vmail_messages, encoded_state[40], encoded_state[43], encoded_state[26],
        data.Total_intl_charge, encoded_state[14], data.CScalls_Rate    
    ]
    # Standardize the features
    standardized_features = scaler.transform([features])
    # Make prediction
    prediction = model.predict(standardized_features)[0]

    
    return {"prediction": int(prediction)}

