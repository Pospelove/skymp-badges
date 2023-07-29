from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pybadges import badge
from httpx import AsyncClient
from typing import List, Dict

app = FastAPI()

BASE_URL = "https://sweetpie.nic11.xyz/api/servers"


async def get_data_from_api(client: AsyncClient, url: str) -> List[Dict]:
    try:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_players_online(servers: List[Dict]) -> int:
    return sum(server["online"] for server in servers)


async def get_servers_online(servers: List[Dict]) -> int:
    return len(servers)


@app.get("/badges/players_online.svg")
async def get_players_online_badge():
    async with AsyncClient() as client:
        servers = await get_data_from_api(client, BASE_URL)
        num_players_online = await get_players_online(servers)
    data = badge(left_text='Players Online', right_text=str(num_players_online), right_color='green')
    return Response(content=data, media_type="image/svg+xml")


@app.get("/badges/servers_online.svg")
async def get_servers_online_badge():
    async with AsyncClient() as client:
        servers = await get_data_from_api(client, BASE_URL)
        num_servers_online = await get_servers_online(servers)
    data = badge(left_text='Servers Online', right_text=str(num_servers_online), right_color='green')
    return Response(content=data, media_type="image/svg+xml")
