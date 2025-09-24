from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import httpx, os

TEAMGERMANY_API = os.getenv("TEAMGERMANY_API", "https://example.com/calculate")

class Anfrage(BaseModel):
    sparte: str = Field(..., pattern="^(strom|gas)$")
    plz: str
    jahresverbrauch_kwh: int
    einzug_am: str | None = None
    zahlweise: str | None = None
    zaehlerart: str | None = None
    anbieter_alt: str | None = None

app = FastAPI()

@app.get("/")
def alive():
    return {"ok": True}

@app.post("/tarifrechner")
async def tarifrechner(a: Anfrage):
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.post(TEAMGERMANY_API, json=a.dict())
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Rechner nicht erreichbar: {e}")
