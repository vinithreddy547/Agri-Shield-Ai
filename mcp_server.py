"""
AgriShield AI: Model Context Protocol (MCP) Server

This module implements an MCP server using the python `mcp` SDK.
It exposes AgriShield's telemetry lookup layers as tools, allowing any MCP-compliant 
LLM client or AI agent to fetch agricultural weather, crop, pathogen, and 
market data directly.
"""

import os
import pandas as pd
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("AgriShield Telemetry")

def lookup_data(file_path: str, query_dict: dict) -> dict:
    """Helper to query localized database tables safely."""
    try:
        if not os.path.exists(file_path):
            return {"error": f"Database file not found: {file_path}"}
        
        df = pd.read_csv(file_path)
        # Apply filters case-insensitively
        filtered = df
        for col, val in query_dict.items():
            if col in filtered.columns and isinstance(val, str):
                filtered = filtered[filtered[col].str.lower() == val.lower()]
                
        if filtered.empty:
            return {"status": "No matching records found.", "query": query_dict}
        return filtered.iloc[0].to_dict()
    except Exception as e:
        return {"error": f"Data lookup execution failure: {str(e)}"}

@mcp.tool()
def get_weather_telemetry(location: str) -> str:
    """
    Fetch localized weather telemetry and risk indexes (temperature, humidity, rainfall, risk level, and forecast).
    
    Args:
        location: The target location (e.g. 'California Central Valley', 'Andhra Pradesh Hub')
    """
    res = lookup_data("data/weather.csv", {"location": location})
    return str(res)

@mcp.tool()
def get_crop_agronomy(crop_type: str, growth_stage: str) -> str:
    """
    Fetch crop phenotype benchmarks and water requirements based on growth stages.
    
    Args:
        crop_type: Cultivated crop type (e.g. 'Corn', 'Rice', 'Almonds')
        growth_stage: Phenological stage (e.g. 'Vegetative', 'Flowering')
    """
    res = lookup_data("data/crop.csv", {"crop_type": crop_type, "growth_stage": growth_stage})
    return str(res)

@mcp.tool()
def get_pathogen_profile(crop_type: str) -> str:
    """
    Fetch plant disease details, primary triggers, and preventative protocols for a crop type.
    
    Args:
        crop_type: Crop type name (e.g. 'Corn', 'Rice')
    """
    res = lookup_data("data/disease.csv", {"crop_type": crop_type})
    return str(res)

@mcp.tool()
def get_market_price(crop_type: str) -> str:
    """
    Fetch regional pricing benchmarks, demand indexes, and price forecasts.
    
    Args:
        crop_type: Crop type name (e.g. 'Corn', 'Rice')
    """
    res = lookup_data("data/market.csv", {"crop_type": crop_type})
    return str(res)

if __name__ == "__main__":
    # Start the MCP server using standard SSE or stdio transport protocol
    mcp.run()
