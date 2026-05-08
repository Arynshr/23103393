import httpx
from config import BASE_URL, API_TOKEN


headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}


async def fetch_depots():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/depots",
            headers=headers
        )
        response.raise_for_status()
        return response.json()["depots"]


async def fetch_vehicles():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/vehicles",
            headers=headers
        )
        response.raise_for_status()
        return response.json()["vehicles"]
