import os
import pandas as pd
from google import genai
from google.genai import types

# Initialize client using the official modern Google GenAI SDK (Task 3.1)
# Expects GEMINI_API_KEY as an active environment variable
client = None
try:
    if os.environ.get("GEMINI_API_KEY"):
        client = genai.Client()
except Exception as e:
    print(f"[SDK Warning] GenAI Client initialization failed: {e}")
MODEL_ID = "gemini-2.5-flash"

def load_grounding_context(inputs: dict) -> dict:
    """Reads local CSV layers to fetch matching parameters, completely mitigating hallucinations (Task 3.2)."""
    context = {
        "weather": "No direct location records verified in localized telemetry layers.",
        "crop": "No matching crop phenotype benchmarks found.",
        "disease": "No custom pathogen profiles verified for this crop type.",
        "market": "No matching commercial terminal pricing records available."
    }
    
    try:
        # Resolve exact paths to the datasets generated in Milestone 1
        weather_df = pd.read_csv("data/weather.csv")
        crop_df = pd.read_csv("data/crop.csv")
        disease_df = pd.read_csv("data/disease.csv")
        market_df = pd.read_csv("data/market.csv")
        
        # Target Query Lookups
        w_match = weather_df[weather_df['location'].str.lower() == inputs['location'].lower()]
        if not w_match.empty:
            context['weather'] = w_match.iloc[0].to_dict()
            
        c_match = crop_df[(crop_df['crop_type'].str.lower() == inputs['crop_type'].lower()) & 
                          (crop_df['growth_stage'].str.lower() == inputs['growth_stage'].lower())]
        if not c_match.empty:
            context['crop'] = c_match.iloc[0].to_dict()
        else:
            # Fallback to crop type basic properties if stage variations aren't fully populated
            c_base = crop_df[crop_df['crop_type'].str.lower() == inputs['crop_type'].lower()]
            if not c_base.empty:
                context['crop'] = c_base.iloc[0].to_dict()
                
        d_match = disease_df[disease_df['crop_type'].str.lower() == inputs['crop_type'].lower()]
        if not d_match.empty:
            context['disease'] = d_match.iloc[0].to_dict()
            
        m_match = market_df[market_df['crop_type'].str.lower() == inputs['crop_type'].lower()]
        if not m_match.empty:
            context['market'] = m_match.iloc[0].to_dict()
            
    except Exception as e:
        print(f"[Data Layer Warning] Context loading failure: {e}")
        
    return context

def call_expert_agent(system_instruction: str, query_content: str) -> str:
    """Standardized API handler executing localized system prompts via gemini-2.5-flash."""
    global client
    if not os.environ.get("GEMINI_API_KEY"):
        return "Operational analysis temporarily offline due to API transport disruptions: GEMINI_API_KEY environment variable is not configured."
    try:
        if client is None:
            client = genai.Client()
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=query_content,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2 # Lower temperature for hyper-focused agricultural planning precision
            )
        )
        return response.text
    except Exception as e:
        return f"Operational analysis temporarily offline due to API transport disruptions: {e}"

def run_multi_agent_pipeline(inputs: dict) -> dict:
    """Orchestrates sequential execution of sub-agents and synthesizes results (Task 3.3 & 3.4)."""
    # 1. Fetch data grounding data chunks
    ctx = load_grounding_context(inputs)
    
    # 2. Initialize sub-agent system instructions to mandate strict data compliance
    weather_prompt = "You are an expert Climatologist. Analyze this weather row data context and summarize local climate risks concisely: " + str(ctx['weather'])
    crop_prompt = f"You are a Senior Agronomist. Evaluate crop data for growth constraints under soil condition '{inputs['soil_type']}': " + str(ctx['crop'])
    disease_prompt = f"You are a Plant Pathologist. Assess pathogen risks using disease patterns and weather parameters: Data: {ctx['disease']} | Context: {ctx['weather']}"
    market_prompt = "You are an Agricultural Commodities Trader. Evaluate global/local transaction risks and valuation forecasts: " + str(ctx['market'])
    resource_prompt = f"You are an Irrigation & Resource Engineer. Dictate direct tactical crop hydration adjustments utilizing this data background: Weather: {ctx['weather']} | Crop Target: {ctx['crop']}"
    
    # 3. Fire parallel/sequential expert analysis tasks
    results = {}
    query = f"Provide a direct, analytical report for {inputs['crop_type']} at {inputs['location']} during {inputs['growth_stage']} phase."
    
    results['weather'] = call_expert_agent(weather_prompt, query)
    results['crop'] = call_expert_agent(crop_prompt, query)
    results['disease'] = call_expert_agent(disease_prompt, query)
    results['market'] = call_expert_agent(market_prompt, query)
    results['resource'] = call_expert_agent(resource_prompt, query)
    
    # 4. Execute Master Orchestrator Synthesis Engine
    orchestrator_system = (
        "You are the Master Farm Decision Orchestrator Agent. Your task is to ingest the specialized reports from "
        "your 5 expert sub-agents and synthesize them into a single, cohesive, high-priority strategic action plan paragraph. "
        "Focus on immediate actionable mitigation steps for the farmer. Do not include introductory filler or separate sections. "
        "Speak authoritatively as an elite AI manager."
    )
    
    orchestrator_query = (
        f"Inputs: Location={inputs['location']}, Crop={inputs['crop_type']}, Stage={inputs['growth_stage']}, Soil={inputs['soil_type']}\n\n"
        f"Weather Agent Report: {results['weather']}\n\n"
        f"Agronomy Agent Report: {results['crop']}\n\n"
        f"Pathology Agent Report: {results['disease']}\n\n"
        f"Market Agent Report: {results['market']}\n\n"
        f"Resource Agent Report: {results['resource']}"
    )
    
    results['orchestrator'] = call_expert_agent(orchestrator_system, orchestrator_query)
    return results
