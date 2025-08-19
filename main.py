from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# Mock storage (in-memory)
farmers: Dict[str, dict] = {}
disasters: Dict[str, dict] = {}
claims: Dict[str, dict] = {}

# Models
class Farmer(BaseModel):
    farmer_id: str
    name: str
    location: str
    crop: str

class Disaster(BaseModel):
    disaster_id: str
    region: str

class Claim(BaseModel):
    claim_id: str
    farmer_id: str
    disaster_id: str
    damage: str

# 1. Register Farmer
@app.post("/farmer/register")
def register_farmer(farmer: Farmer):
    farmers[farmer.farmer_id] = farmer.dict()
    return {"status": "registered", "farmer": farmer}

# 2. Declare Disaster
@app.post("/disaster/declare")
def declare_disaster(disaster: Disaster):
    disasters[disaster.disaster_id] = disaster.dict()
    return {"status": "disaster declared", "disaster": disaster}

# 3. Submit Claim
@app.post("/claim/submit")
def submit_claim(claim: Claim):
    if claim.farmer_id not in farmers:
        return {"status": "rejected", "reason": "Farmer not found"}

    if claim.disaster_id not in disasters:
        return {"status": "rejected", "reason": "Disaster not declared"}

    # Simple auto-verification: if farmer's location == disaster region → approve
    farmer_location = farmers[claim.farmer_id]["location"]
    disaster_region = disasters[claim.disaster_id]["region"]

    if farmer_location == disaster_region:
        status = "approved"
    else:
        status = "pending"

    claims[claim.claim_id] = {
        "farmer_id": claim.farmer_id,
        "disaster_id": claim.disaster_id,
        "damage": claim.damage,
        "status": status,
    }

    return {"status": status, "claim": claims[claim.claim_id]}

# 4. Check Claim Status
@app.get("/claim/status/{claim_id}")
def check_status(claim_id: str):
    if claim_id not in claims:
        return {"status": "not found"}
    return {"claim_id": claim_id, "status": claims[claim_id]["status"]}
