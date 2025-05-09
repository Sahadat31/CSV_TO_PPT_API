from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def generate_summary(df: str) -> str:
    prompt = f"""You're a data analyst. Summarize the patterns in this dataset and only provide the summary as output.
    Please keep in mind I will use the summary directly in a ppt, so format the summary in that way only:
    \n\n{df}"""
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt
    )
    return response.text

def extract_insights(df: str) -> list[str]:
    prompt = f"""You're a data scientist. Give me detailed insights from this data, don't provide anything else.
    It would be great if you sepearate each insight with some specific special character like '****'. It would help me to parse the output.:
    \n\n{df}"""
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt
    )
    return response.text.split("****")[1:]
