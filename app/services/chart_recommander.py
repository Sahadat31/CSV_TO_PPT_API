from google import genai
import json
import os
import pandas as pd
from dotenv import load_dotenv
from typing import List
from services.chart_spec import ChartSpec

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def recommend_charts(df: pd.DataFrame) -> List[ChartSpec]:
    print(df.columns)
    preview = {
        "columns": [
            {
                "name": c,
                "dtype": str(df[c].dtype),
                "n_unique": int(df[c].nunique())
            }
            for c in df.columns if c 
        ]
    }
    print("🔍 Schema Preview for LLM:\n", json.dumps(preview, indent=2))
    prompt = f"""
        You’re a data analyst. Given this DataFrame schema:

        {json.dumps(preview, indent=2)}

        Recommend 3–5 chart specs in JSON.  
        Each spec should include:
        - type: one of 'time_series','bar','histogram'
        - x: column for the x-axis
        - y: column for y-axis (if applicable)
        - any extra params like max_categories.

        Return ONLY a JSON array of these specs.
        """
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt
    )
    print(response.text)
    raw_text = response.text.strip()

    # Remove markdown code block markers
    if raw_text.startswith("```json"):
        raw_text = raw_text[len("```json"):].strip()
    if raw_text.startswith("```"):
        raw_text = raw_text[len("```"):].strip()
    if raw_text.endswith("```"):
        raw_text = raw_text[:-3].strip()
    try:
        specs = json.loads(raw_text)
        return specs
    except json.JSONDecodeError:
        raise ValueError("LLM did not return valid JSON")
    
