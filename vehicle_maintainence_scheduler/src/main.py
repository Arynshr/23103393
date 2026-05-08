from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from app_client import (
    fetch_depots,
    fetch_vehicles
)
app = FastAPI(
    title="Vehicle Maintenance Scheduler"
)

@app.get("/")
async def root():
    return {"message": "Vehicle Scheduler Running"}


class Vehicle(BaseModel):
    TaskID: str
    Duration: int
    Impact: int


class Depot(BaseModel):
    ID: int
    MechanicHours: int


class SelectedVehicle(BaseModel):
    TaskID: str
    Duration: int
    Impact: int


class ScheduleResponse(BaseModel):
    depot_id: int
    total_impact: int
    total_duration: int
    selected_tasks: List[SelectedVehicle]
    
    
def optimize_schedule(vehicles, max_hours):
    n = len(vehicles)

    dp = [[0] * (max_hours + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        duration = vehicles[i - 1]["Duration"]
        impact = vehicles[i - 1]["Impact"]

        for h in range(max_hours + 1):

            if duration <= h:
                dp[i][h] = max(
                    impact + dp[i - 1][h - duration],
                    dp[i - 1][h]
                )
            else:
                dp[i][h] = dp[i - 1][h]

    selected = []
    h = max_hours

    for i in range(n, 0, -1):
        if dp[i][h] != dp[i - 1][h]:
            vehicle = vehicles[i - 1]
            selected.append(vehicle)
            h -= vehicle["Duration"]

    selected.reverse()

    total_duration = sum(v["Duration"] for v in selected)

    return {
        "total_impact": dp[n][max_hours],
        "total_duration": total_duration,
        "selected_tasks": selected
    }
    
    
@app.get("/schedule")
async def generate_schedule():

    depots = await fetch_depots()
    vehicles = await fetch_vehicles()

    results = []

    for depot in depots:

        optimized = optimize_schedule(
            vehicles,
            depot["MechanicHours"]
        )

        results.append({
            "depot_id": depot["ID"],
            **optimized
        })

    return {
        "success": True,
        "results": results
    }
