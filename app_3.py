
import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from joblib import load

import pandas as pd
from io import StringIO

from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker

from datetime import datetime 
import pytz
import os


#SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:GRplpdmGkIRHEYvzqDFKzdnNXepPqdEz@centerbeam.proxy.rlwy.net:11297/railway"
SQLALCHEMY_DATABASE_URL = os.environ["SQLALCHEMY_DATABASE_URL"]

#SQLALCHEMY_DATABASE_URL1 = "mysql+pymysql://root:KSvwNhzjIaKIozHAwswNeHaqEWpbRGrL@ballast.proxy.rlwy.net:37847/railway"
SQLALCHEMY_DATABASE_URL1 = os.environ["SQLALCHEMY_DATABASE_URL1"]

engine = create_engine(SQLALCHEMY_DATABASE_URL)
engine1 = create_engine(SQLALCHEMY_DATABASE_URL1)

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

@app.get("/db-check")
def verify_db_connections():
    try:
        # Validamos la primera base de datos usando su motor directamente
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            
        # Validamos la segunda base de datos usando su motor directamente
        with engine1.connect() as connection1:
            connection1.execute(text("SELECT 1"))
        
        return {
            "status": "success",
            "message": "Connected to both databases successfully."
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": f"Failed to connect to databases. Error: {str(e)}"
            }
        )
    
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
    }
    )

    df.to_sql(
        "inputs",
        con=engine1,
        if_exists="append",
        index=False 
    )

    predictions_df.to_sql(
        "predictions",
        con=engine,
        if_exists="append",
        index=False 
    )


    return {
        "inputs": df.to_dict(orient="records"),
        "predictions": predictions.tolist()
    }