import os
import pandas as pd
from google import genai
from google.genai import types

# Initialize client safely (must be instantiated, though it won't be used if key is missing)
client = genai.Client()

# ==========================================
# 2. LOCAL DATA GROUNDING TOOLS
# ==========================================

def get_weather_data(location):
    """Filters weather.csv by location matching. Returns dict or None."""
    file_path = "data/weather.csv"
    if not os.path.exists(file_path):
        return None
    try:
        df = pd.read_csv(file_path)
        match = df[df['location'].str.lower() == location.strip().lower()]
        if not match.empty:
            return match.iloc[0].to_dict()
    except Exception as e:
        print(f"Error reading weather data: {e}")
    return None

def get_crop_data(crop_type, growth_stage):
    """Filters crop.csv by crop_type and growth_stage. Returns dict or None."""
    file_path = "data/crop.csv"
    if not os.path.exists(file_path):
        return None
    try:
        df = pd.read_csv(file_path)
        match = df[
            (df['crop_type'].str.lower() == crop_type.strip().lower()) & 
            (df['growth_stage'].str.lower() == growth_stage.strip().lower())
        ]
        if not match.empty:
            return match.iloc[0].to_dict()
        
        # Fallback: if growth_stage doesn't match, get first match of crop_type
        match_crop = df[df['crop_type'].str.lower() == crop_type.strip().lower()]
        if not match_crop.empty:
            return match_crop.iloc[0].to_dict()
    except Exception as e:
        print(f"Error reading crop data: {e}")
    return None

def get_disease_data(crop_type):
    """Filters disease.csv for relevant pathologies. Returns list of dicts."""
    file_path = "data/disease.csv"
    if not os.path.exists(file_path):
        return []
    try:
        df = pd.read_csv(file_path)
        match = df[df['crop_type'].str.lower() == crop_type.strip().lower()]
        if not match.empty:
            return match.to_dict(orient='records')
    except Exception as e:
        print(f"Error reading disease data: {e}")
    return []

def get_market_data(crop_type):
    """Filters market.csv for regional pricing and trends. Returns dict or None."""
    file_path = "data/market.csv"
    if not os.path.exists(file_path):
        return None
    try:
        df = pd.read_csv(file_path)
        match = df[df['crop_type'].str.lower() == crop_type.strip().lower()]
        if not match.empty:
            return match.iloc[0].to_dict()
    except Exception as e:
        print(f"Error reading market data: {e}")
    return None


# Helper function to call Gemini or fallback
def _call_gemini_agent(system_instruction: str, prompt: str, fallback_content: str) -> str:
    # If API key is not configured, return fallback directly
    if not os.environ.get("GEMINI_API_KEY"):
        return fallback_content
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2
            )
        )
        return response.text.strip()
    except Exception as e:
        return f"{fallback_content} (Gemini fallback triggered: {e})"


# ==========================================
# 3. MULTI-AGENT PROMPT LOGIC FUNCTIONS
# ==========================================

def run_weather_agent(weather_row):
    """Climate & Weather Tracker sub-agent."""
    system_instruction = (
        "You are the Climate & Weather Tracker sub-agent for AgriShield AI. "
        "Analyze the provided weather data. Summarize the temperature, humidity, "
        "rainfall, and risk level in 1-2 professional sentences, starting with "
        "an alert if risk level is High or Medium."
    )
    prompt = f"Weather data: {weather_row}"
    
    # Dynamic fallback string matching requested mock behavior
    loc = weather_row.get('location', 'Specified Area')
    temp = weather_row.get('temperature_c', 38.2)
    hum = weather_row.get('humidity_pct', 20)
    risk = weather_row.get('climate_risk_level', 'High')
    forecast = weather_row.get('forecast_summary', 'Incoming extreme heatwave')
    
    fallback = f"🌦️ [MOCK] Alert for {loc}: {forecast}. Temperatures projected to hit {temp}°C. Relative humidity at a dry {hum}%."
    return _call_gemini_agent(system_instruction, prompt, fallback)


def run_crop_health_agent(crop_row):
    """Crop Health Analyst sub-agent."""
    system_instruction = (
        "You are the Crop Health Analyst sub-agent for AgriShield AI. "
        "Analyze the crop's development metrics (ideal soil, growth stage, "
        "daily water requirement, baseline yield). Synthesize this into 1-2 "
        "clear, actionable sentences."
    )
    prompt = f"Crop health data: {crop_row}"
    
    crop = crop_row.get('crop_type', 'Corn')
    stage = crop_row.get('growth_stage', 'Vegetative')
    water = crop_row.get('daily_water_requirement_liters', 5.5)
    yield_base = crop_row.get('baseline_yield_ton_per_acre', 4.5)
    
    fallback = f"🌱 [MOCK] Target stage: {stage}. Current daily requirement: {water} Liters/plant. Baseline yield benchmark is {yield_base} tons/acre."
    return _call_gemini_agent(system_instruction, prompt, fallback)


def run_disease_agent(disease_rows, weather_context):
    """Disease Vector Predictor sub-agent."""
    system_instruction = (
        "You are the Disease Vector Predictor sub-agent for AgriShield AI. "
        "Evaluate the listed diseases and their triggers against the current "
        "weather parameters (temperature, humidity). Estimate the disease outbreak "
        "risk level (High/Medium/Low) and explain your reasoning in 1-2 sentences."
    )
    prompt = f"Diseases: {disease_rows}\nWeather context: {weather_context}"
    
    # We evaluate weather to determine a mock risk statement
    temp = float(weather_context.get('temperature_c', 25.0))
    hum = float(weather_context.get('humidity_pct', 50))
    
    if hum > 80 and temp > 20:
        fallback = "🦠 [MOCK] Risk Level: High. Wet and warm weather conditions are highly conducive to fungal infections. Initiate preventative fungicide protocol."
    else:
        fallback = "🦠 [MOCK] Risk Level: Low. Fungal triggers require cool, damp conditions (<25°C), whereas current localized forecast shows high dry heat."
        
    return _call_gemini_agent(system_instruction, prompt, fallback)


def run_market_agent(market_row):
    """Market Price Forecaster sub-agent."""
    system_instruction = (
        "You are the Market Price Forecaster sub-agent for AgriShield AI. "
        "Summarize current pricing per ton, demand index, and forecasted price trend "
        "for the crop in 1-2 concise, professional sentences."
    )
    prompt = f"Market data: {market_row}"
    
    price = market_row.get('current_price_per_ton', 4200.0)
    trend = market_row.get('price_trend_forecast', 'Increasing')
    
    fallback = f"💰 [MOCK] Current Valuations: ${price:,.2f}/ton. Trend: {trend}. Strong global export signals due to supply deficits."
    return _call_gemini_agent(system_instruction, prompt, fallback)


def run_resource_agent(weather_context, crop_context):
    """Resource Allocation Planner sub-agent."""
    system_instruction = (
        "You are the Resource Allocation Planner sub-agent for AgriShield AI. "
        "Formulate dynamic, localized directives (irrigation adjustments, "
        "fertilizer application, protective actions) in 1-2 sentences using "
        "the crop's water requirements and current weather data."
    )
    prompt = f"Weather: {weather_context}\nCrop: {crop_context}"
    
    temp = float(weather_context.get('temperature_c', 25.0))
    
    if temp > 35:
        fallback = "💧 [MOCK] Dynamic Directives: Increase drip-line frequency by 25%. Maintain current soil nitrogen metrics to prevent late-stage crop stress."
    else:
        fallback = "💧 [MOCK] Dynamic Directives: Keep normal irrigation schedule. Verify soil moisture index is at baseline level."
        
    return _call_gemini_agent(system_instruction, prompt, fallback)


# ==========================================
# 4. THE MASTER FARM DECISION ORCHESTRATOR
# ==========================================

def run_master_orchestrator(location, crop_type, growth_stage, soil_type):
    """
    Coordinates data tools, runs the 5 sub-agents sequentially, and synthesizes 
    their responses using a Master Orchestrator prompt to generate a single strategic briefing.
    """
    # 1. Coordinate data tools with safe fallbacks
    weather_row = get_weather_data(location)
    if not weather_row:
        weather_row = {
            "location": location,
            "date": "N/A",
            "temperature_c": 38.2,
            "humidity_pct": 20,
            "rainfall_mm": 0.0,
            "climate_risk_level": "High",
            "forecast_summary": "No local records. Defaulting to Central Valley summer defaults (heatwave risk)."
        }
        
    crop_row = get_crop_data(crop_type, growth_stage)
    if not crop_row:
        crop_row = {
            "crop_type": crop_type,
            "ideal_soil": soil_type,
            "growth_stage": growth_stage,
            "daily_water_requirement_liters": 5.5,
            "baseline_yield_ton_per_acre": 4.5
        }
        
    disease_rows = get_disease_data(crop_type)
    if not disease_rows:
        disease_rows = [{
            "crop_type": crop_type,
            "disease_name": "Standard Pathogens",
            "primary_symptoms": "Leaf spots/rot",
            "weather_trigger_condition": "High humidity (>85%) and temperature (<25C)",
            "prevention_protocol": "Monitor humidity and manage plant density."
        }]
        
    market_row = get_market_data(crop_type)
    if not market_row:
        market_row = {
            "crop_type": crop_type,
            "current_price_per_ton": 4200.0,
            "demand_index": 0.90,
            "market_region": "Global Export",
            "price_trend_forecast": "Increasing due to regional weather disruptions"
        }

    # 2. Run the 5 specialized sub-agents sequentially
    weather_insight = run_weather_agent(weather_row)
    crop_insight = run_crop_health_agent(crop_row)
    disease_insight = run_disease_agent(disease_rows, weather_row)
    market_insight = run_market_agent(market_row)
    resource_insight = run_resource_agent(weather_row, crop_row)

    # 3. Master Synthesis Prompt
    system_instruction = (
        "You are the Master Farm Decision Orchestrator for AgriShield AI. "
        "Review the structured inputs from five specialized sub-agents. "
        "Synthesize these findings into a single, cohesive, high-priority "
        "strategic briefing paragraph (3-4 sentences) for the farmer. "
        "Prioritize immediate actions, risk factors, and financial impact."
    )
    
    prompt = f"""
    Farm Parameters:
    - Location: {location}
    - Crop: {crop_type}
    - Stage: {growth_stage}
    - Soil: {soil_type}

    Sub-Agent Insights:
    1. Climate & Weather Tracker: {weather_insight}
    2. Crop Health Analyst: {crop_insight}
    3. Disease Vector Predictor: {disease_insight}
    4. Market Price Forecaster: {market_insight}
    5. Resource Allocation Planner: {resource_insight}
    """
    
    # Fetch demand index if available
    demand = market_row.get('demand_index', 0.90)
    
    orchestrator_fallback = (
        f"👉 [ORCHESTRATOR MOCK DATA] High priority action required: "
        f"Schedule immediate targeted irrigation. High heatwave thresholds expected in the next 48 hours "
        f"will compound current {growth_stage.lower()} water deficits. Market demand indices remain high ({demand}), "
        f"making yield protection critical."
    )
    
    orchestrator_insight = _call_gemini_agent(system_instruction, prompt, orchestrator_fallback)

    # 4. Return results dictionary mapped to the dashboard layout
    return {
        "weather": weather_insight,
        "crop": crop_insight,
        "disease": disease_insight,
        "market": market_insight,
        "resource": resource_insight,
        "orchestrator": orchestrator_insight
    }
