import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime

from computer_use_demo.tools.time import GetUTCTimeTool, SleepTool, ToolError


@pytest.fixture
def get_utc_time_tool():
    return GetUTCTimeTool()


@pytest.fixture
def sleep_tool():
    return SleepTool()


@pytest.mark.asyncio
async def test_get_utc_time():
    tool = GetUTCTimeTool()
    with patch('datetime.datetime') as mock_datetime:
        mock_now = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.timezone.utc = datetime.timezone.utc
        mock_datetime.now.return_value.strftime.return_value = "2024-01-01 12:00:00 UTC"
        
        result = await tool()
        assert result.output == "2024-01-01 12:00:00 UTC"


@pytest.mark.asyncio
async def test_sleep():
    tool = SleepTool()
    with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
        result = await tool(duration=5)
        mock_sleep.assert_called_once_with(5)
        assert result.output == "Slept for 5 seconds"


@pytest.mark.asyncio
async def test_sleep_missing_duration():
    tool = SleepTool()
    with pytest.raises(ToolError, match="duration parameter is required"):
        await tool()


@pytest.mark.asyncio
async def test_sleep_negative_duration():
    tool = SleepTool()
    with pytest.raises(ToolError, match="duration must be non-negative"):
        await tool(duration=-1)


def test_get_utc_time_tool_params():
    tool = GetUTCTimeTool()
    params = tool.to_params()
    assert params["name"] == "get_utc_time"
    assert "description" in params
    assert params["input_schema"]["type"] == "object"


def test_sleep_tool_params():
    tool = SleepTool()
    params = tool.to_params()
    assert params["name"] == "sleep"
    assert "description" in params
    assert params["input_schema"]["type"] == "object"
    assert "duration" in params["input_schema"]["properties"]
    assert params["input_schema"]["required"] == ["duration"]
