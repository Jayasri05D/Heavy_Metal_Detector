from fastapi import FastAPI, UploadFile, File
import pandas as pd
from calculations import calculate_HPI, calculate_HEI
from database import SessionLocal, WaterResult

app = FastAPI()

# Example permissible limits (mg/L)
STANDARDS = {"Pb": 0.01, "Cd": 0.003, "As": 0.01}

@app.post("/calculate/")
async def calculate(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    db = SessionLocal()
    results = []

    for _, row in df.iterrows():
        concentrations = {m: row[m] for m in STANDARDS if m in row}
        hpi = calculate_HPI(concentrations, STANDARDS)
        hei = calculate_HEI(concentrations, STANDARDS)

        # Save to local SQLite
        new_result = WaterResult(
            latitude=row.get("Latitude"),
            longitude=row.get("Longitude"),
            hpi=hpi,
            hei=hei,
            synced=0
        )
        db.add(new_result)
        db.commit()
        db.refresh(new_result)

        results.append({
            "location": {"lat": row.get("Latitude"), "lon": row.get("Longitude")},
            "HPI": hpi,
            "HEI": hei
        })

    db.close()
    return {"results": results}
