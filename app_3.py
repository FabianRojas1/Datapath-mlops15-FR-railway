
import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from joblib import load

import pandas as pd
from io import StringIO

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from datetime import datetime 
import pytz
import os

SQLALCHEMY_DATABASE_URL = "mysql://root:GRplpdmGkIRHEYvzqDFKzdnNXepPqdEz@centerbeam.proxy.rlwy.net:11297/railway"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

metadata = MetaData()

Sessionlocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
    )

app = FastAPI()

def get_db():
    db = Sessionlocal()
    try :
        yield db 
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "hello world"}

@app.get("/health", status_code=200)
def health_check(db=Depends(get_db)):
    return {"status": "ok"}



@app.post("/predict")
async def predict_backnote(file : UploadFile = File(...)):
    classifier = load("linear_regression.joblib")
    
    features_df = pd.read_csv("selected_features.csv")
    features = features_df["0"].tolist()

    content = await file.read()
    df = pd.read_csv(StringIO(content.decode("utf-8")))
    df = df[features]

    predictions = classifier.predict(df)

    bog_tz = pytz.timezone("America/Bogota")
    now = datetime.now(bog_tz)

    predictions_df = pd.DataFrame({
        'file_name': file.filename,
        'predictions': predictions,
        'created_at': now
    })

    predictions_df.to_sql(
        "predictions",
        con=engine,
        if_exists="append",
        index=False 
    )

    return {
        "predictions": predictions.tolist()
    }