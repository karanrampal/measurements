"""Unit tests for api"""

import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.anyio
async def test_get_measurements() -> None:
    """Test response code"""
    async with AsyncClient(app=app, base_url="http://test") as asc:
        response = await asc.post("/measurement/")
    assert response.status_code == 422
