"""Time-related tools for system operations."""

import asyncio
import datetime
from typing import Any

from anthropic.types.beta import BetaToolParam

from .base import BaseAnthropicTool, ToolError, ToolResult


class GetUTCTimeTool(BaseAnthropicTool):
    """A tool that returns the current UTC time."""

    name = "get_utc_time"

    def to_params(self) -> BetaToolParam:
        return {
            "name": self.name,
            "description": "Get the current UTC time",
            "input_schema": {
                "type": "object",
                "properties": {}
            }
        }

    async def __call__(self, **kwargs) -> ToolResult:
        current_time = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        return ToolResult(output=current_time)


class SleepTool(BaseAnthropicTool):
    """A tool that pauses execution for a specified number of seconds."""

    name = "sleep"

    def to_params(self) -> BetaToolParam:
        return {
            "name": self.name,
            "description": "Pause execution for specified number of seconds",
            "input_schema": {
                "type": "object",
                "properties": {
                    "duration": {
                        "type": "number",
                        "description": "Number of seconds to sleep",
                        "minimum": 0
                    }
                },
                "required": ["duration"]
            }
        }

    async def __call__(self, duration: float | None = None, **kwargs) -> ToolResult:
        if duration is None:
            raise ToolError("duration parameter is required")
        if duration < 0:
            raise ToolError("duration must be non-negative")
            
        await asyncio.sleep(duration)
        return ToolResult(output=f"Slept for {duration} seconds")
