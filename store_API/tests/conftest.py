from typing import AsyncGenerator ,Generator
import pytest
#interact with api with out starting fastapi
from fastapi.testclient import TestClient
#to make request
from httpx import AsyncClient

from store_API.main import app
from store_API.routers import post_table,comment_table

#runs once for entire test session
#asyncio creates platform to run async function
@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'

@pytest.fixture
def client() -> Generator:
    yield TestClient(app)


#runs for every test
@pytest.fixture(autouse=True)
async def db()-> AsyncGenerator:
    post_table.clear()
    comment_table.clear()
    yield


@pytest.fixture
async def async_client(Client)-> AsyncGenerator:
    async with AsyncClient(app=app,base_url=client.base_url) as ac:
        yield ac